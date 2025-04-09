# Next.js Image Gallery on AWS ECS

## Overview
This project is a **Next.js-based image gallery** that fetches images from an **AWS API Gateway endpoint** and displays them in an attractive frontend. The application is containerized using **Docker**, stored in **Amazon ECR**, and deployed to **AWS ECS** for scalable hosting.

## Features
- Fetches images from an API Gateway URL
- Displays images in a responsive gallery
- Deployed on AWS ECS using a containerized Next.js app
- Uses Amazon ECR for container storage

## Architecture
1. **Frontend**: Next.js application
2. **Backend**: AWS API Gateway serves image URLs
3. **Containerization**: Dockerized Next.js app stored in Amazon ECR
4. **Hosting**: ECS Fargate for scalable and serverless deployment

## Prerequisites
Before deploying, ensure you have:
- AWS Account
- AWS CLI installed and configured
- Docker installed
- A Next.js project ready to be containerized
- API Gateway endpoint for fetching images

## Deployment Steps
### 1. Containerizing the Next.js App
```sh
# Build the Next.js project
npm run build

# Create a Docker image
docker build -t nextjs-image-gallery .

# Authenticate Docker with ECR
aws ecr get-login-password --region <your-region> | docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.<your-region>.amazonaws.com

# Tag the Docker image
docker tag nextjs-image-gallery:latest <aws_account_id>.dkr.ecr.<your-region>.amazonaws.com/nextjs-image-gallery:latest

# Push to ECR
docker push <aws_account_id>.dkr.ecr.<your-region>.amazonaws.com/nextjs-image-gallery:latest
```

### 2. Deploying to ECS via AWS Console
1. Go to **ECS Console** → **Create a Cluster** → Select **Fargate**.
2. Create a **Task Definition** with:
   - Task Role: `ecsTaskExecutionRole` (with ECR access)
   - Container Image: `ECR image URL`
   - Port Mapping: `3000:3000`
3. Create an **ECS Service** under your cluster:
   - Set Task Definition
   - Desired tasks: `1` (or more for scaling)
   - Configure Load Balancer if needed
4. Deploy the service and test the application.

## Configuration
- **API Gateway URL**: Update `NEXT_PUBLIC_API_URL` in `.env.local`.
```env
NEXT_PUBLIC_API_URL=https://px893gsmql.execute-api.us-east-1.amazonaws.com/images
```
- **Port Configuration**: Ensure `EXPOSE 3000` is set in `Dockerfile`.

## Future Enhancements
- Implement CI/CD pipeline with AWS CodePipeline
- Add caching mechanism for faster image loading
- Use AWS CloudFront for global content delivery

## Author
**Pravesh Sudha** - [praveshsudha.com](https://praveshsudha.com)

## License
This project is licensed under the MIT License.

