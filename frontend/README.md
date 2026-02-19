# Frontend - EPG Training Feedback Loop

This project was generated using [Angular CLI](https://github.com/angular/angular-cli) version 21.1.3.

## Prerequisites

- **Node.js**: 18.x or higher
- **npm**: 9.x or higher
- **Backend Server**: The backend API must be running on `http://localhost:8000`

## Quick Start

### 1. Install Dependencies

```bash
npm install
```

### 2. Start Backend Server

**IMPORTANT**: The frontend requires the backend to be running first.

```bash
# In a separate terminal, navigate to backend directory
cd ../backend

# Activate virtual environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Start the backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Verify backend is running by visiting: http://localhost:8000/health

### 3. Start Frontend Development Server

```bash
# In the frontend directory
ng serve
```

Once the server is running, open your browser and navigate to `http://localhost:4200/`. The application will automatically reload whenever you modify any of the source files.

## API Proxy Configuration

The frontend is configured to proxy all `/api` requests to the backend server at `http://localhost:8000`. This is configured in:
- `proxy.conf.json` - Proxy configuration file
- `angular.json` - References the proxy config in the serve options

## Code scaffolding

Angular CLI includes powerful code scaffolding tools. To generate a new component, run:

```bash
ng generate component component-name
```

For a complete list of available schematics (such as `components`, `directives`, or `pipes`), run:

```bash
ng generate --help
```

## Building

To build the project run:

```bash
ng build
```

This will compile your project and store the build artifacts in the `dist/` directory. By default, the production build optimizes your application for performance and speed.

## Running unit tests

To execute unit tests with the [Vitest](https://vitest.dev/) test runner, use the following command:

```bash
ng test
```

## Running end-to-end tests

For end-to-end (e2e) testing, run:

```bash
ng e2e
```

Angular CLI does not come with an end-to-end testing framework by default. You can choose one that suits your needs.

## Troubleshooting

### "Failed to Start Session" Error

**Symptom**: Clicking "Start Session" shows an error in the action log.

**Solution**:
1. **Verify backend is running**:
   ```bash
   # Test backend health endpoint
   curl http://localhost:8000/health
   # Expected response: {"status":"ok"}
   ```

2. **Check browser console** (F12 → Console tab):
   - Look for network errors or CORS issues
   - Check the Network tab for failed `/api/sessions/start` requests

3. **Verify proxy is working**:
   ```bash
   # With frontend dev server running, test proxy
   curl http://localhost:4200/api/health
   # Expected response: {"status":"ok"}
   ```

4. **Restart frontend dev server**:
   - Stop the dev server (Ctrl+C)
   - Run `ng serve` again
   - Look for "Proxy created" message in console

### Backend Connection Issues

If you see CORS errors or connection refused:
- Ensure backend is running on port 8000
- Check that `proxy.conf.json` points to the correct backend URL
- Verify no firewall is blocking localhost connections

### Video Not Loading

- Ensure `video.mp4` exists in `frontend/public/assets/`
- Check browser console for 404 errors
- Verify the video format is supported (MP4, WebM, MOV)

## Additional Resources

For more information on using the Angular CLI, including detailed command references, visit the [Angular CLI Overview and Command Reference](https://angular.dev/tools/cli) page.

