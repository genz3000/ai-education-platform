# AI Education Platform - Frontend

## Project Structure

```
frontend/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── (auth)/            # Auth pages (login, register)
│   │   ├── (dashboard)/       # Main dashboard
│   │   │   ├── teacher/       # Teacher portal
│   │   │   ├── student/       # Student portal
│   │   │   ├── parent/        # Parent portal
│   │   │   └── admin/         # Admin portal
│   │   ├── api/               # API routes (proxy)
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── components/
│   │   ├── ui/                # Base UI components (shadcn)
│   │   ├── knowledge/         # Knowledge base components
│   │   ├── qa/                # Q&A components
│   │   ├── assessment/        # Assessment components
│   │   └── analytics/         # Analytics components
│   ├── hooks/                 # Custom React hooks
│   ├── lib/                   # Utilities
│   ├── services/              # API services
│   ├── stores/                # Zustand stores
│   ├── types/                 # TypeScript types
│   └── styles/                # Global styles
├── public/
│   ├── locales/               # i18n translation files
│   └── images/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
└── package.json
```

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript 5
- **UI**: TailwindCSS + shadcn/ui
- **State Management**: Zustand
- **Data Fetching**: TanStack Query (React Query)
- **Forms**: React Hook Form + Zod
- **i18n**: next-intl
- **Testing**: Vitest + Playwright

## Getting Started

```bash
# Install dependencies
npm install

# Copy environment variables
cp .env.example .env.local

# Start development server
npm run dev

# Build for production
npm run build

# Run tests
npm run test
```

## Environment Variables

```env
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_WS_URL=ws://localhost:8000

# Auth
NEXT_PUBLIC_AUTH_PROVIDER=credentials
NEXTAUTH_SECRET=your-secret-key
NEXTAUTH_URL=http://localhost:3000

# Analytics
NEXT_PUBLIC_GA_ID=your-ga-id

# Feature Flags
NEXT_PUBLIC_ENABLE_AI_FEATURES=true
NEXT_PUBLIC_MAX_UPLOAD_SIZE=50
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/auth/login` | POST | User login |
| `/api/v1/auth/logout` | POST | User logout |
| `/api/v1/knowledge/search` | GET | Search knowledge base |
| `/api/v1/qa/ask` | POST | Ask AI question |
| `/api/v1/assessment/generate` | POST | Generate assessment |
| `/api/v1/analytics/student/{id}` | GET | Get student analytics |

## Development Guidelines

### Code Style
- Use TypeScript strict mode
- Follow ESLint + Prettier configuration
- Write self-documenting code

### Component Structure
```
Component/
├── index.tsx          # Main component
├── variants.ts        # Variant definitions
├── types.ts           # Component types
└── test.tsx           # Unit tests
```

### Testing
- Unit tests for utilities and hooks
- Integration tests for API routes
- E2E tests for critical user flows

## Deployment

### Docker
```bash
docker build -t ai-education-frontend .
docker run -p 3000:3000 ai-education-frontend
```

### Kubernetes
```bash
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/frontend-service.yaml
```