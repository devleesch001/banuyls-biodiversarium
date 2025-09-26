# Banyuls Biodiversarium

A comprehensive AI-powered biodiversity monitoring system for aquariums, featuring species detection, identification, and educational interfaces.

## 🌊 Project Overview

The Banyuls Biodiversarium is an integrated system designed to automatically detect and identify marine species in aquarium environments. It combines artificial intelligence, web interfaces, and real-time monitoring to provide an interactive educational experience for visitors while assisting researchers in biodiversity documentation.

### Key Features

- **AI-Powered Species Detection**: Real-time identification of marine species using YOLOv6
- **Web Application**: Responsive interface for visitors to identify species through photos
- **Admin Interface**: Management system for species database and user permissions
- **Interactive Kiosk**: Dedicated interface for aquarium installations
- **Multi-language Support**: Available in French, English, and Catalan
- **Real-time Monitoring**: Live species detection for continuous monitoring

## 🏗️ System Architecture

The system consists of 6 main services orchestrated with Docker Compose:

### Core Services

1. **Web Application (`fish-hub`)** - React/TypeScript
   - Responsive web interface for species identification
   - Camera integration for photo capture
   - Species documentation and search functionality
   - Multi-language support (FR, EN, CA)

2. **Backend API (`back-fish`)** - Python/Flask
   - Species database management
   - User authentication and authorization
   - API endpoints for web and AI services
   - Admin interface for content management

3. **AI Service (`ia`)** - Python/FastAPI
   - YOLOv6-based species detection model
   - Image processing and analysis
   - Real-time and batch detection endpoints
   - Model training and optimization tools

4. **Interactive Kiosk (`born`)** - React
   - Dedicated interface for aquarium installations
   - Touch-friendly interface design
   - Real-time species monitoring display

5. **Video Proxy Services** - Node.js
   - RTSP to HTTP streaming conversion
   - CORS handling for video feeds
   - Real-time video processing pipeline

6. **Web Server (`webserver`)** - Nginx
   - Reverse proxy and load balancing
   - SSL/TLS termination
   - Static file serving

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Git with submodule support
- Minimum 8GB RAM (16GB recommended for AI training)
- GPU support recommended for optimal AI performance

### Installation

1. **Clone the repository with submodules:**
```bash
git clone --recursive https://github.com/devleesch001/banuyls-biodiversarium.git
cd banuyls-biodiversarium
```

2. **Start all services:**
```bash
docker-compose up -d
```

Or using newer Docker Compose syntax:
```bash
docker compose up -d
```

3. **Access the applications:**
   - Web Application: http://localhost (port 80)
   - Admin Interface: http://localhost/admin
   - API Documentation: http://localhost/api/docs
   - AI Service: http://localhost:333/docs

### Development Setup

For development with hot reloading:
```bash
docker-compose -f docker-compose-dev.yml up -d
```

For GPU-accelerated AI training:
```bash
docker-compose -f docker-compose-gpu.yml up -d
```

## 📋 Service Details

### Web Application (fish-hub)
- **Technology**: React 18, TypeScript, Material-UI
- **Features**: Camera integration, responsive design, PWA support
- **Port**: 111 (internal), 80 (via nginx)
- **Documentation**: [web-appli/README.md](web-appli/README.md)

### Backend API (back-fish)
- **Technology**: Python, Flask, SQLAlchemy
- **Features**: REST API, user management, species database
- **Port**: 222 (internal), 80 (via nginx)
- **Default Admin**: username: `admin`, password: `admin`
- **Documentation**: [back-fish/README.md](back-fish/README.md)

### AI Service (analyze-fish)
- **Technology**: Python, FastAPI, YOLOv6, PyTorch
- **Features**: Species detection, model training, quantization
- **Port**: 333 (internal), 80 (via nginx)
- **API Endpoints**:
  - `GET /ia/` - Health check
  - `POST /ia/v1.0/image-detection/` - Single image analysis
  - `POST /ia/v1.0/live-detection/` - Real-time detection
- **Documentation**: [analyze-fish/README.md](analyze-fish/README.md)

### Interactive Kiosk (born)
- **Technology**: React, responsive design
- **Features**: Touch interface, real-time monitoring
- **Port**: 444 (internal), 80 (via nginx)

### Video Services
- **HTTP CORS Proxy**: Port 8000
- **RTSP to HTTP**: Ports 8001, 8002
- **Features**: Video streaming, format conversion

## 🔧 Configuration

### Environment Variables

#### Web Application
- `REACT_APP_API_URL`: Backend API URL (default: auto-detected)

#### Backend API
- `IA_URL`: AI service URL (default: `http://ia/ia`)

#### Interactive Kiosk
- `PORT`: Service port (default: 80)
- `REACT_APP_API_URL`: Backend API URL

### SSL/TLS Configuration

For production deployment with SSL:

1. **Initialize Certbot (dry run):**
```bash
docker-compose run --rm certbot certonly --webroot --webroot-path /var/www/certbot/ --dry-run -d your-domain.com
```

2. **Generate SSL certificates:**
```bash
docker-compose run --rm certbot certonly --webroot --webroot-path /var/www/certbot/ -d your-domain.com
```

## 🗃️ Database

- **Type**: SQLite (development) / PostgreSQL (production)
- **Location**: `./database/` directory
- **Persistence**: Data persists across container restarts
- **Backup**: Regular backups recommended for production

## 📊 Monitoring & Logs

View service logs:
```bash
docker-compose logs -f [service-name]
```

Monitor resource usage:
```bash
docker stats
```

Health checks:
- Web Application: `http://localhost/health`
- Backend API: `http://localhost/api/health`
- AI Service: `http://localhost:333/ia/`

## 🔨 Development

### Adding New Species

1. Access the admin interface at `http://localhost/admin`
2. Login with admin credentials
3. Navigate to species management
4. Add species with images and documentation

### Training Custom Models

See [analyze-fish/docs/Train_custom_data.md](analyze-fish/docs/Train_custom_data.md) for detailed instructions.

### API Integration

The system provides RESTful APIs for integration:

- **Species Detection**: `POST /api/mobile/analyze`
- **Species Information**: `GET /api/species/{scientific_name}`
- **Species List**: `GET /api/species`

## 🐛 Troubleshooting

### Common Issues

1. **Services not starting**: Check Docker daemon and available resources
2. **AI model loading slowly**: Ensure sufficient RAM and consider GPU acceleration
3. **Database connection errors**: Verify database volume permissions
4. **Image detection failing**: Check AI service logs and model weights

### Debug Mode

Enable verbose logging:
```bash
docker-compose up -d --build
docker-compose logs -f
```

### Performance Optimization

- Use GPU acceleration for AI services
- Increase memory allocation for training
- Optimize image sizes for faster processing
- Use production builds for deployment

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes to relevant submodules
4. Test with Docker Compose
5. Submit a pull request

### Development Guidelines

- Follow component-specific coding standards
- Update documentation for new features
- Test across different environments
- Maintain backward compatibility

## 📄 License

This project contains multiple components with individual licenses. See individual component README files for specific license information.

## 🏛️ Acknowledgments

- Developed for the Banyuls-sur-Mer Marine Observatory
- AI models based on YOLOv6 architecture
- Built with modern web technologies and containerization

## 📞 Support

For technical support or questions:
1. Check component-specific documentation
2. Review Docker Compose logs
3. Consult troubleshooting section
4. Create an issue in the repository

---

**Note**: This is a research and educational project. Ensure proper configuration and security measures for production deployments.

