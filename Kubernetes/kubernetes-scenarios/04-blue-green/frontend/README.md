# Blue-Green Frontend

## Project Structure & Best Practices

- **Production code** lives in the `src/` directory. Only production code is included in the Docker build.
- **Test files** (e.g., `*.test.tsx`) are located in the `__tests__/` directory at the project root. This keeps the production build clean and ensures tests are not bundled into the Docker image.
- A `.dockerignore` file is used to exclude `node_modules`, `__tests__`, and other dev-only files from the Docker build context for faster, smaller, and more secure images.

## Running Locally

- **Install dependencies:**
  ```sh
  npm install
  # or
  yarn install
  ```
- **Run the development server:**
  ```sh
  npm start
  # or
  yarn start
  ```
- **Run tests:**
  ```sh
  npm test
  # or
  yarn test
  ```
  Jest will automatically pick up tests from the `__tests__/` directory.

## Building for Production (Docker)

- **Build the Docker image:**
  ```sh
  docker build -t bluegreen-frontend:latest .
  ```
- The Docker build will only include production code from `src/` and will not include test or dev files, ensuring a clean, reliable, and fast build for demos and deployments.

---

**Contributing?**
- Place all new tests in `__tests__/`.
- Keep production code in `src/`.
- This structure ensures a world-class demo and learning experience for everyone! 