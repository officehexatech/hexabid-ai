import pika
import json
import logging
from typing import Dict, Any, Callable, Optional
from datetime import datetime
import uuid
from config.rabbitmq_config import (
    RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_USER, RABBITMQ_PASSWORD,
    RABBITMQ_VHOST, EXCHANGE_AGENTS, EXCHANGE_ORCHESTRATION, EXCHANGE_SYSTEM
)

logger = logging.getLogger(__name__)

class EventBus:
    """Event bus for agent communication using RabbitMQ"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.connection = None
            self.channel = None
            self.initialized = False
    
    def connect(self) -> bool:
        """Establish connection to RabbitMQ"""
        try:
            credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
            parameters = pika.ConnectionParameters(
                host=RABBITMQ_HOST,
                port=RABBITMQ_PORT,
                virtual_host=RABBITMQ_VHOST,
                credentials=credentials,
                connection_attempts=3,
                retry_delay=2,
                socket_timeout=5.0,
                heartbeat=600,
                blocked_connection_timeout=300
            )
            
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
            
            # Declare exchanges
            self._setup_topology()
            
            self.initialized = True
            logger.info(f"Connected to RabbitMQ at {RABBITMQ_HOST}:{RABBITMQ_PORT}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            return False
    
    def _setup_topology(self):
        """Setup exchanges and queues"""
        # Declare exchanges
        self.channel.exchange_declare(
            exchange=EXCHANGE_AGENTS,
            exchange_type='topic',
            durable=True
        )
        
        self.channel.exchange_declare(
            exchange=EXCHANGE_ORCHESTRATION,
            exchange_type='direct',
            durable=True
        )
        
        self.channel.exchange_declare(
            exchange=EXCHANGE_SYSTEM,
            exchange_type='topic',
            durable=True
        )
        
        logger.info("RabbitMQ topology setup complete")
    
    def publish_event(self, event_type: str, data: Dict[str, Any], exchange: str = EXCHANGE_AGENTS, routing_key: str = None) -> str:
        """Publish an event to the event bus"""
        if not self.initialized:
            if not self.connect():
                raise Exception("Failed to connect to event bus")
        
        event_id = str(uuid.uuid4())
        event = {
            'event_id': event_id,
            'event_type': event_type,
            'timestamp': datetime.utcnow().isoformat(),
            'data': data
        }
        
        if routing_key is None:
            routing_key = f"agent.{event_type}"
        
        try:
            self.channel.basic_publish(
                exchange=exchange,
                routing_key=routing_key,
                body=json.dumps(event),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # Persistent
                    content_type='application/json',
                    correlation_id=event_id
                )
            )
            
            logger.info(f"Event published: {event_type} with ID {event_id}")
            return event_id
            
        except Exception as e:
            logger.error(f"Failed to publish event: {e}")
            raise
    
    def subscribe_to_queue(self, queue_name: str, callback: Callable, routing_key: str = '#'):
        """Subscribe to a queue and process messages"""
        if not self.initialized:
            if not self.connect():
                raise Exception("Failed to connect to event bus")
        
        # Declare queue
        self.channel.queue_declare(queue=queue_name, durable=True)
        
        # Bind to exchange
        self.channel.queue_bind(
            queue=queue_name,
            exchange=EXCHANGE_AGENTS,
            routing_key=routing_key
        )
        
        # Set QoS
        self.channel.basic_qos(prefetch_count=1)
        
        def on_message(ch, method, properties, body):
            try:
                event = json.loads(body.decode())
                logger.info(f"Processing event: {event.get('event_type')}")
                
                result = callback(event)
                
                if result:
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                else:
                    ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
                    
            except Exception as e:
                logger.error(f"Error processing message: {e}")
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
        
        self.channel.basic_consume(
            queue=queue_name,
            on_message_callback=on_message,
            auto_ack=False
        )
        
        logger.info(f"Subscribed to queue: {queue_name}")
    
    def start_consuming(self):
        """Start consuming messages"""
        if not self.initialized:
            raise Exception("Event bus not initialized")
        
        logger.info("Starting event consumer...")
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()
            self.close()
    
    def close(self):
        """Close connection"""
        if self.connection and not self.connection.is_closed:
            self.connection.close()
            logger.info("Event bus connection closed")

# Global event bus instance
event_bus = EventBus()
