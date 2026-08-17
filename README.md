# RSRoute
> Self-hostable FastAPI gateway providing a unified REST API for multiple LLM providers powered by LangChain.


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