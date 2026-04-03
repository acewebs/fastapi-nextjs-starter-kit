# Contributing

Thanks for your interest in contributing! This project is open source and welcomes contributions.

## How to Contribute

### Reporting Bugs

Open an [issue](../../issues/new?template=bug_report.md) with:
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Docker version, etc.)

### Suggesting Features

Open an [issue](../../issues/new?template=feature_request.md) with:
- What problem it solves
- Proposed approach (if any)

### Submitting Code

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-change`
3. Make your changes
4. Run the checks:
   ```bash
   ./dev/toolbox/run lint
   ./dev/toolbox/run test
   ```
5. Commit with a clear message
6. Push and open a Pull Request

### Pull Request Guidelines

- Keep PRs focused — one feature or fix per PR
- Ensure `lint` and `test` pass (CI will verify)
- Update docs if your change affects usage
- Add tests for new API endpoints

## Development Setup

See [docs/development.md](docs/development.md) for local setup instructions.

## Project Structure

| Directory | Description |
|-----------|-------------|
| `api/` | FastAPI backend |
| `web/` | Next.js frontend |
| `worker/` | ARQ background worker |
| `dev/toolbox/` | Development CLI |
| `docs/` | Documentation |

## Code Style

- **Python**: Formatted with `ruff`, type-checked with `mypy`
- **TypeScript**: Linted with ESLint, type-checked with `tsc`
- Run `./dev/toolbox/run format` to auto-format Python code

## Questions?

Open a [discussion](../../discussions) or an issue. We're happy to help.
