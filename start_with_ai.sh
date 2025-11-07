#!/bin/bash

# Quick Setup Script for AI Image Generation Feature

echo "================================================"
echo "Django Recipe App - AI Image Setup"
echo "================================================"
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✓ Created .env file"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and add your Hugging Face API token!"
    echo "   Get a free token at: https://huggingface.co/settings/tokens"
    echo ""
else
    echo "✓ .env file already exists"
    echo ""
fi

# Check if HUGGINGFACE_API_TOKEN is set
if grep -q "HUGGINGFACE_API_TOKEN=your_token_here" .env 2>/dev/null || ! grep -q "HUGGINGFACE_API_TOKEN=" .env 2>/dev/null; then
    echo "⚠️  WARNING: Hugging Face API token not configured!"
    echo "   Edit .env and replace 'your_token_here' with your actual token"
    echo "   Get one free at: https://huggingface.co/settings/tokens"
    echo ""
else
    echo "✓ Hugging Face API token is configured"
    echo ""
fi

echo "Running Django server..."
echo "Once started, you can:"
echo "  1. Go to http://127.0.0.1:8000/"
echo "  2. Log in or create an account"
echo "  3. Create or edit a recipe"
echo "  4. Click 'Generate AI Image' button"
echo ""
echo "================================================"
echo ""

python manage.py runserver
