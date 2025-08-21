import os
from dotenv import load_dotenv
from agents import (
    AsyncOpenAI, 
    OpenAIChatCompletionsModel,
    Agent,
    Runner,
    RunContextWrapper,
    RunConfig,
    TResponseInputItem,
     set_tracing_disabled,
     input_guardrail,
     output_guardrail,
     GuardrailFunctionOutput,
     InputGuardrailTripwireTriggered,
     OutputGuardrailTripwireTriggered
    )
from pydantic import BaseModel
def main():
    load_dotenv()
    set_tracing_disabled(True)

    
    key = os.getenv("GEMINI_API_KEY")
    base_url = os.getenv("base_url")
    gemini_client=AsyncOpenAI(api_key=key,base_url=base_url)
    Model=OpenAIChatCompletionsModel(model="gemini-2.5-flash",openai_client=gemini_client)
    config=RunConfig(
        model=Model,
        model_provider=gemini_client,
        tracing_disabled=True
    )
    class MathHomeworkOutput(BaseModel):
        is_math_homework: bool
        reasoning: str
        answer: str
    class PoliticsRealtedOutput(BaseModel):
        is_politics_realted: bool
        reasoning: str
        answer: str
    #Appling input guardrail    
    inputGuardrailsAgent=Agent (
        name="inputGuardrailsAgent",
        instructions="you have to check either th user's Query is realted to math",
        output_type=MathHomeworkOutput,
        model=Model
    )
    
    @input_guardrail
    async def math_guardrail(ctx: RunContextWrapper[None], agent: Agent, input: str|list[TResponseInputItem]
    )->GuardrailFunctionOutput:
        
        result = await Runner.run(inputGuardrailsAgent, input,context=ctx.context)
        print("\n\n[GUARDRAIL_RESPONSE]",result.final_output)
        
        return GuardrailFunctionOutput(
            output_info=result.final_output,
            tripwire_triggered=result.final_output.is_math_homework,
        )
    

    




    OutputGuardrailsAgent=Agent (
        name="OutputGuardrailsAgent",
        instructions="you have to check either th user's Query is realted to Politics",
        output_type=PoliticsRealtedOutput,
        model=Model
    )
    @output_guardrail
    async def politics_guardrail(ctx: RunContextWrapper[None], agent: Agent, input: str|list[TResponseInputItem]
        )->GuardrailFunctionOutput:
            
            result = await Runner.run(OutputGuardrailsAgent, input,context=ctx.context)
            print("\n\n[GUARDRAIL_RESPONSE]",result.final_output)
            
            return GuardrailFunctionOutput(
                output_info=result.final_output,
                tripwire_triggered=result.final_output.is_politics_realted,
            )
    agent=Agent(
        name="Math homework Assistant",
        instructions="you are customer support agent who facilitate customers with math homework assistant.",
        model=Model,
        input_guardrails=[math_guardrail],
        output_guardrails=[politics_guardrail]
    ) 
    try:
        res=Runner.run_sync(starting_agent=agent,input="TELL ME politcain zulfikar ali bhutto")
        print(res.final_output)
    except InputGuardrailTripwireTriggered :   
        print("This is math work")
    except OutputGuardrailTripwireTriggered as e:
        print("Output tripwire triggered: Output contains political content.",e)
if __name__ == "__main__":
    main()