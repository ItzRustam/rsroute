# RSRoute
> Self-hostable FastAPI gateway providing a unified REST API for multiple LLM providers powered by LangChain.

## ☕ Support the Developer

Building and maintaining **rsroute** takes a lot of time and effort! If this project helped you out, please consider chipping in to keep it growing.

[![GitHub Sponsor](https://img.shields.io/badge/Sponsor-GitHub-ea4aaa?style=for-the-badge&logo=github)](https://github.com/sponsors/ItzRustam)
[![Ko-fi](https://img.shields.io/badge/Support-Ko--fi-F16061?style=for-the-badge&logo=ko-fi)](https://ko-fi.com/itzrustam)

## Project is still in development.

## Why RSRoute?

Without RSRoute:

Project A:  
    ├── Setup Mistral client  
    ├── Setup OpenRouter client  
    ├── Manage API keys  
    └── Handle provider errors  

Project B:  
    ├── Setup Mistral client  
    ├── Setup OpenRouter client  
    ├── Manage API keys  
    └── Handle provider errors  
  
Project C:  
    └── Repeat everything again...  


With RSRoute:

        Project A
        Project B
        Project C
            |
            v
          RSRoute
            |
            v
       LLM Providers

## What RSRoute provides

- Centralized API key management
- Unified access to multiple LLM providers
- Simple REST API
- Authentication layer
- Provider abstraction powered by LangChain

## you know you can click on that star on corner and make it golden try it out :)

```
@software{RSRoute,
  author = {Rustam Bhadouriya (ItzRustam)},
  year = {2026},
  title = {RSRoute: Unified API Routing for Large Language Model Providers},
  url = {https://github.com/ItzRustam/RSRoute}
}
```
