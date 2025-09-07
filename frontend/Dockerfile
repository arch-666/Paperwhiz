# Stage 1: Build
FROM node:18-bullseye-slim AS builder
WORKDIR /app

# Copy package files and install dependencies
COPY package.json package-lock.json ./
RUN npm ci

# Copy source code
COPY . .

# Build the Next.js app
RUN npm run build

# Stage 2: Production
FROM node:18-bullseye-slim
WORKDIR /app

# Copy build output and node_modules
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/node_modules ./node_modules
COPY package.json ./  

# Expose port and start
EXPOSE 3000
CMD ["npm", "start"]
