import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { TypeOrmModule } from '@nestjs/typeorm';

// const { POSTGRES_HOST, POSTGRES_PORT, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB } = process.env;
const ENTITIES = [];

@Module({
  imports: [
    TypeOrmModule.forRoot({ // TODO: Move this to a separate file so we can use the .env file
      type: 'postgres',
      host: 'localhost',
      port: 5342,
      username: 'postgres',
      password: 'password',
      database: 'postgres',
      entities: ENTITIES,
      synchronize: true,
    }),
    TypeOrmModule.forFeature(ENTITIES),
  ],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
