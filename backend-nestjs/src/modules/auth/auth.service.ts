import {
  Injectable,
  UnauthorizedException,
  BadRequestException,
} from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { JwtService } from '@nestjs/jwt';
import { ConfigService } from '@nestjs/config';
import * as bcrypt from 'bcrypt';
import { User } from '../../database/entities/user.entity';
import { Role } from '../../database/entities/role.entity';

@Injectable()
export class AuthService {
  constructor(
    @InjectRepository(User)
    private userRepository: Repository<User>,
    @InjectRepository(Role)
    private roleRepository: Repository<Role>,
    private jwtService: JwtService,
    private configService: ConfigService,
  ) {}

  async sendOtp(email: string): Promise<void> {
    // Generate 6-digit OTP
    const otp = Math.floor(100000 + Math.random() * 900000).toString();

    // Hash OTP
    const otpHash = await bcrypt.hash(otp, 10);

    // Find or create user
    let user = await this.userRepository.findOne({ where: { email } });

    if (!user) {
      // Auto-create user on first login
      user = this.userRepository.create({
        email,
        fullName: email.split('@')[0],
        status: 'active',
      });
    }

    // Update OTP details
    user.otpHash = otpHash;
    user.otpExpiresAt = new Date(Date.now() + 5 * 60 * 1000); // 5 minutes
    user.otpAttempts = 0;

    await this.userRepository.save(user);

    // Send email (mock for now - integrate SendGrid later)
    console.log(`OTP for ${email}: ${otp}`);
    // TODO: Integrate SendGrid
    // await this.sendEmailViaS endGrid(email, otp);
  }

  async verifyOtp(
    email: string,
    otp: string,
  ): Promise<{
    user: any;
    accessToken: string;
    refreshToken: string;
    expiresIn: number;
  }> {
    const user = await this.userRepository.findOne({
      where: { email },
      relations: ['role'],
    });

    if (!user) {
      throw new UnauthorizedException('User not found');
    }

    if (!user.otpHash || !user.otpExpiresAt) {
      throw new UnauthorizedException('No OTP requested');
    }

    if (new Date() > user.otpExpiresAt) {
      throw new UnauthorizedException('OTP expired');
    }

    if (user.otpAttempts >= 3) {
      throw new UnauthorizedException('Too many failed attempts');
    }

    // Verify OTP
    const isValid = await bcrypt.compare(otp, user.otpHash);

    if (!isValid) {
      user.otpAttempts += 1;
      await this.userRepository.save(user);
      throw new UnauthorizedException('Invalid OTP');
    }

    // Clear OTP
    user.otpHash = null;
    user.otpExpiresAt = null;
    user.otpAttempts = 0;
    user.lastLoginAt = new Date();
    await this.userRepository.save(user);

    // Generate tokens
    const payload = {
      sub: user.id,
      email: user.email,
      role: user.role?.name,
    };

    const accessToken = this.jwtService.sign(payload);
    const refreshToken = this.jwtService.sign(payload, {
      secret: this.configService.get('JWT_REFRESH_SECRET'),
      expiresIn: this.configService.get('JWT_REFRESH_EXPIRES_IN', '7d'),
    });

    return {
      user: {
        id: user.id,
        email: user.email,
        fullName: user.fullName,
        role: user.role?.name,
      },
      accessToken,
      refreshToken,
      expiresIn: 3600,
    };
  }

  async refreshToken(
    refreshToken: string,
  ): Promise<{ accessToken: string; expiresIn: number }> {
    try {
      const payload = this.jwtService.verify(refreshToken, {
        secret: this.configService.get('JWT_REFRESH_SECRET'),
      });

      const newAccessToken = this.jwtService.sign({
        sub: payload.sub,
        email: payload.email,
        role: payload.role,
      });

      return {
        accessToken: newAccessToken,
        expiresIn: 3600,
      };
    } catch (error) {
      throw new UnauthorizedException('Invalid refresh token');
    }
  }

  async validateUser(userId: string): Promise<User> {
    return this.userRepository.findOne({
      where: { id: userId },
      relations: ['role'],
    });
  }
}
