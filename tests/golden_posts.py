from datetime import UTC, datetime

from backend.models.feed_schemas import FeedPost

_D = datetime(2026, 6, 1, tzinfo=UTC)

GOLDEN_POSTS: list[FeedPost] = [
    FeedPost(
        id="j01",
        title="Meta releases Llama 4 with 405B parameters and MoE architecture",
        author="test",
        url="https://reddit.com/r/MachineLearning/j01",  # type: ignore[arg-type]
        created_at=_D,
        source="reddit",
        clean_body_text=(
            "Meta AI has open-sourced Llama 4, a 405-billion-parameter model using a "
            "mixture-of-experts (MoE) architecture. The model achieves 89.2 % on MMLU "
            "and outperforms GPT-4o on several coding benchmarks. Weights are available "
            "under a custom licence allowing commercial use for companies with fewer than "
            "700 million monthly active users."
        ),
    ),
    FeedPost(
        id="j02",
        title="Google DeepMind publishes AlphaFold 3 predicting all biomolecules",
        author="test",
        url="https://reddit.com/r/MachineLearning/j02",  # type: ignore[arg-type]
        created_at=_D,
        source="reddit",
        clean_body_text=(
            "DeepMind's AlphaFold 3 extends its predecessor to predict the joint structure "
            "of proteins, DNA, RNA, and small molecules. The model uses a diffusion-based "
            "architecture and achieves state-of-the-art accuracy on the PoseBusters benchmark. "
            "It is available via a web server for non-commercial academic use."
        ),
    ),
    FeedPost(
        id="j03",
        title="Anthropic raises $4 B from Google at $18 B valuation",
        author="test",
        url="https://reddit.com/r/artificial/j03",  # type: ignore[arg-type]
        created_at=_D,
        source="reddit",
        clean_body_text=(
            "Anthropic, the AI safety company behind Claude, closed a $4 billion investment "
            "from Google, bringing its total valuation to $18 billion. The funding will be used "
            "to expand compute infrastructure and safety research. Google becomes one of "
            "Anthropic's largest shareholders alongside Amazon."
        ),
    ),
    FeedPost(
        id="j04",
        title="EU AI Act enters into force — high-risk AI systems face strict rules",
        author="test",
        url="https://reddit.com/r/technology/j04",  # type: ignore[arg-type]
        created_at=_D,
        source="reddit",
        clean_body_text=(
            "The European Union AI Act has officially entered into force, imposing obligations "
            "on providers of high-risk AI systems including biometric identification, critical "
            "infrastructure, and employment screening tools. Non-compliance can result in fines "
            "of up to 30 million euros or 6 % of global annual turnover."
        ),
    ),
    FeedPost(
        id="j05",
        title="vLLM 0.5 improves inference throughput 2× with PagedAttention v2",
        author="test",
        url="https://reddit.com/r/MachineLearning/j05",  # type: ignore[arg-type]
        created_at=_D,
        source="reddit",
        clean_body_text=(
            "The vLLM team released version 0.5, featuring PagedAttention v2 which reduces "
            "KV-cache fragmentation and delivers 2× higher throughput on Llama-3-70B compared "
            "with the previous release. The update also adds speculative decoding and multi-LoRA "
            "serving support. Benchmarks show 18,000 tokens/sec on 8×A100 hardware."
        ),
    ),
    FeedPost(
        id="j06",
        title="OpenAI launches o3-mini reasoning model at $0.15 per 1 M tokens",
        author="test",
        url="https://reddit.com/r/OpenAI/j06",  # type: ignore[arg-type]
        created_at=_D,
        source="reddit",
        clean_body_text=(
            "OpenAI released o3-mini, a cost-efficient reasoning model priced at $0.15 per "
            "million input tokens. The model scores 87.3 % on AIME 2024 and 79.7 % on "
            "SWE-bench Verified. It is available via API and supports function calling and "
            "structured outputs. Average response latency is 8 seconds for complex tasks."
        ),
    ),
    FeedPost(
        id="j07",
        title="Hugging Face releases SmolLM2-1.7B — runs on-device on smartphones",
        author="test",
        url="https://reddit.com/r/MachineLearning/j07",  # type: ignore[arg-type]
        created_at=_D,
        source="reddit",
        clean_body_text=(
            "Hugging Face released SmolLM2-1.7B, a compact language model optimised for "
            "on-device inference. The model achieves 62.4 % on HellaSwag and 49.1 % on "
            "ARC-Challenge while running at 30 tokens/sec on an iPhone 15 Pro. It is "
            "released under Apache 2.0 and supports 4-bit quantisation via llama.cpp."
        ),
    ),
    FeedPost(
        id="j08",
        title="Microsoft integrates GitHub Copilot into Azure DevOps pipelines",
        author="test",
        url="https://reddit.com/r/programming/j08",  # type: ignore[arg-type]
        created_at=_D,
        source="reddit",
        clean_body_text=(
            "Microsoft announced that GitHub Copilot is now natively integrated into Azure "
            "DevOps, enabling AI-assisted pull-request reviews, pipeline-failure summaries, "
            "and automated issue triage. The feature is in preview for Enterprise customers "
            "at no additional cost and uses GPT-4o under the hood."
        ),
    ),
    FeedPost(
        id="j09",
        title="Mistral releases Mixtral 8×22B — 141 B total parameters, Apache 2.0",
        author="test",
        url="https://reddit.com/r/LocalLLaMA/j09",  # type: ignore[arg-type]
        created_at=_D,
        source="reddit",
        clean_body_text=(
            "Mistral AI open-sourced Mixtral 8×22B, a sparse MoE model with 141 billion "
            "total parameters and 39 billion active per token. It achieves 77.8 % on MMLU "
            "and 75.2 % on HumanEval, outperforming LLaMA 3 70B on most benchmarks. "
            "It supports a 64 k context window and is available on Hugging Face."
        ),
    ),
    FeedPost(
        id="j10",
        title="Stanford proposes Constitutional AI Distillation as RLHF replacement",
        author="test",
        url="https://reddit.com/r/MachineLearning/j10",  # type: ignore[arg-type]
        created_at=_D,
        source="reddit",
        clean_body_text=(
            "A Stanford paper proposes Constitutional AI Distillation (CAD), a method for "
            "aligning language models without human raters. CAD generates preference pairs "
            "using a reward model and achieves comparable safety scores to RLHF on TruthfulQA "
            "and BBQ benchmarks while reducing annotation costs by 90 %. The approach is "
            "compatible with DPO training."
        ),
    ),
    FeedPost(
        id="j11",
        title="Tesla FSD v13 cuts driver interventions by 40 % per internal data",
        author="test",
        url="https://reddit.com/r/technology/j11",  # type: ignore[arg-type]
        created_at=_D,
        source="reddit",
        clean_body_text=(
            "Tesla's Full Self-Driving v13 update, rolled out to North American customers, "
            "reportedly reduces driver interventions by 40 % compared with v12 according to "
            "Tesla's internal fleet telemetry. The update replaces the previous rule-based "
            "planner with an end-to-end neural network. Critics note the figures are "
            "unverified by independent third parties."
        ),
    ),
    FeedPost(
        id="j12",
        title="LangChain 0.3 introduces LangGraph for stateful multi-agent workflows",
        author="test",
        url="https://reddit.com/r/MachineLearning/j12",  # type: ignore[arg-type]
        created_at=_D,
        source="reddit",
        clean_body_text=(
            "LangChain released version 0.3 featuring LangGraph, a framework for stateful "
            "multi-agent systems using a directed-graph model. Developers can define agent "
            "nodes, edges with conditional routing, and shared memory stores. LangGraph "
            "supports checkpointing for long-running workflows and integrates with LangSmith "
            "for tracing."
        ),
    ),
    FeedPost(
        id="j13",
        title="Nvidia announces Blackwell B200 GPU with 20 petaflops for AI training",
        author="test",
        url="https://reddit.com/r/hardware/j13",  # type: ignore[arg-type]
        created_at=_D,
        source="reddit",
        clean_body_text=(
            "Nvidia unveiled the Blackwell B200 GPU delivering 20 petaflops of FP8 compute "
            "and 192 GB of HBM3e memory with 8 TB/s bandwidth. The chip uses a "
            "second-generation transformer engine and targets training of 1-trillion-parameter "
            "models. Cloud-provider shipments are expected in late 2025."
        ),
    ),
    FeedPost(
        id="j14",
        title="AI safety coalition publishes open model spec for frontier AI alignment",
        author="test",
        url="https://reddit.com/r/MachineLearning/j14",  # type: ignore[arg-type]
        created_at=_D,
        source="reddit",
        clean_body_text=(
            "A coalition of AI safety researchers published an open model-specification "
            "document outlining desired properties for frontier AI systems, including "
            "corrigibility, non-deception, and power-seeking avoidance. The spec proposes "
            "formal evaluation criteria and a tiered risk classification system. Several "
            "major labs expressed intent to adopt portions of the framework."
        ),
    ),
    FeedPost(
        id="j15",
        title="Stable Diffusion 3.5 Large improves text rendering and anatomy accuracy",
        author="test",
        url="https://reddit.com/r/StableDiffusion/j15",  # type: ignore[arg-type]
        created_at=_D,
        source="reddit",
        clean_body_text=(
            "Stability AI released Stable Diffusion 3.5 Large, an 8-billion-parameter "
            "text-to-image model with improved text rendering and anatomically correct "
            "human figures. It uses a multimodal diffusion transformer (MMDiT) architecture "
            "and achieves top-3 scores on GenEval. Weights are available under a "
            "non-commercial research licence."
        ),
    ),
    FeedPost(
        id="j16",
        title="Apple Intelligence uses 3 B on-device model on iPhone 16",
        author="test",
        url="https://reddit.com/r/apple/j16",  # type: ignore[arg-type]
        created_at=_D,
        source="reddit",
        clean_body_text=(
            "Apple confirmed that Apple Intelligence uses a 3-billion-parameter on-device "
            "model for most tasks, with Private Cloud Compute handling more complex requests. "
            "The on-device model runs in 512 MB of memory and processes text at 30 tokens/sec "
            "on the iPhone 16's A18 chip. Apple stated that no user data is stored on cloud "
            "servers."
        ),
    ),
    FeedPost(
        id="j17",
        title="Runway Gen-3 Alpha generates 10-second 1080p video from text prompts",
        author="test",
        url="https://reddit.com/r/artificial/j17",  # type: ignore[arg-type]
        created_at=_D,
        source="reddit",
        clean_body_text=(
            "Runway released Gen-3 Alpha, capable of generating 10-second 1080p video clips "
            "from text and image prompts. The model supports camera motion controls including "
            "pan, tilt, and dolly moves. Generation takes roughly 90 seconds via the web "
            "interface. Access is limited to paid subscribers starting at $12 per month."
        ),
    ),
    FeedPost(
        id="j18",
        title="Salesforce acquires Scale AI for $14 B to boost Einstein data pipelines",
        author="test",
        url="https://reddit.com/r/technology/j18",  # type: ignore[arg-type]
        created_at=_D,
        source="reddit",
        clean_body_text=(
            "Salesforce announced the acquisition of Scale AI, the leading data-labelling and "
            "evaluation platform, for $14 billion. Scale AI's technology will be integrated "
            "into Salesforce Einstein to improve model training pipelines. Scale AI CEO "
            "Alexandr Wang will join Salesforce as Chief AI Officer. The deal is subject to "
            "regulatory approval."
        ),
    ),
    FeedPost(
        id="j19",
        title="Cerebras CS-3 wafer-scale chip hits 1 M tokens/sec on Llama-3-70B",
        author="test",
        url="https://reddit.com/r/hardware/j19",  # type: ignore[arg-type]
        created_at=_D,
        source="reddit",
        clean_body_text=(
            "Cerebras Systems demonstrated inference at 1 million tokens per second on "
            "Llama-3-70B using its CS-3 wafer-scale chip. The chip integrates 4 trillion "
            "transistors and 900,000 cores on a single silicon wafer, eliminating inter-chip "
            "communication overhead. API access starts at $0.10 per million tokens."
        ),
    ),
    FeedPost(
        id="j20",
        title="OpenAI launches ChatGPT Edu for universities with GPT-4o and admin controls",
        author="test",
        url="https://reddit.com/r/OpenAI/j20",  # type: ignore[arg-type]
        created_at=_D,
        source="reddit",
        clean_body_text=(
            "OpenAI announced ChatGPT Edu, a university-focused version of ChatGPT that "
            "includes GPT-4o access, unlimited message quotas, and administrator controls "
            "for usage policies. Institutions can deploy custom GPTs for course-specific "
            "assistants. Data from Edu users is not used for model training. Pricing is "
            "negotiated per institution."
        ),
    ),
]
