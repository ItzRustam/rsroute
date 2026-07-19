# rsllm
> Self-hostable FastAPI gateway providing a unified REST API for multiple LLM providers powered by LangChain.


## Why rsllm?

Without rsllm:

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


With rsllm:

        Project A
        Project B
        Project C
            |
            v
          rsllm
            |
            v
       LLM Providers

## What rsllm provides

- Centralized API key management
- Unified access to multiple LLM providers
- Simple REST API
- Authentication layer
- Provider abstraction powered by LangChain