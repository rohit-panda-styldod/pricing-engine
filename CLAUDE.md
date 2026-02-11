# Pricing Engine - Project Guide

## Overview
E-commerce pricing engine handling calculations, discounts, tax, and shipping.

## Tech Stack
- Python 3.10+
- pytest for testing

## Code Conventions
- All functions must have docstrings
- Use type hints where practical
- Keep functions focused and small (single responsibility)
- Input validation is important -- functions should reject invalid inputs
- Round monetary values to 2 decimal places

## Testing
- Run tests: `pytest test_pricing.py -v`
- Every new feature needs tests
- Cover edge cases and boundary conditions
- Test both happy paths and error cases

## Git Conventions
- Branch naming: `feature/<description>` or `fix/<description>`
- Commit messages: imperative mood, concise (e.g., "Add shipping calculator")
- One logical change per commit when possible