
using System.ClientModel;
using DotNetEnv;
using Microsoft.SemanticKernel;

Env.Load();

#pragma warning disable SKEXP0070
#pragma warning disable SKEXP0001

List<string> serviceIds = [];

var builder = Kernel.CreateBuilder();

// Add the Ollama chat completion service
var modelId = "Phi4-mini";
var endpoint = new Uri("http://127.0.0.1:11434/");
builder.AddOllamaChatCompletion(modelId, endpoint, serviceId:"local");

// Add the OpenAI chat completion service
var openAIModelId = Environment.GetEnvironmentVariable("OPENAI_CHAT_MODEL_ID");
var key = Environment.GetEnvironmentVariable("OPENAI_API_KEY");
builder.AddOpenAIChatCompletion(openAIModelId, key, serviceId:"cloud");

// Add the OpenAI chat completion service
var client = new OpenAI.OpenAIClient(new ApiKeyCredential("fake-key"), new OpenAI.OpenAIClientOptions()
{
    Endpoint = new Uri("http://127.0.0.1:5272/v1/")
});

builder.AddOpenAIChatCompletion("Phi-4-mini", client, serviceId:"l2");

// add service IDs
serviceIds.Add("local");
serviceIds.Add("cloud");
serviceIds.Add("l2");


// Add plugins
var kernel = builder.Build();
kernel.Plugins
    .AddFromType<MyTimePlugin>();
kernel.PromptRenderFilters.Add(new SelectedServiceFilter());

// Create a custom router to determine which service to use based on the user's input
var router = new CustomRouter();


Console.Write("> ");

string? input = null;
while ((input = Console.ReadLine()) is not null)
{
    Console.WriteLine();

    KernelArguments arguments = new(new PromptExecutionSettings()
    {
        ServiceId = router.GetService(input, serviceIds), //returns either "local" or "cloud"
        FunctionChoiceBehavior = FunctionChoiceBehavior.Auto()
    });

    try
    {
        var functionResult = await kernel.InvokePromptAsync(input, arguments);
        Console.Write($"\n>>> Result: {functionResult}\n\n> ");
    }
    catch (Exception ex)
    {
        Console.WriteLine($"Error: {ex.Message}\n\n> ");
    }
}



class SelectedServiceFilter : IPromptRenderFilter
{
    /// <inheritdoc/>
    public Task OnPromptRenderAsync(PromptRenderContext context, Func<PromptRenderContext, Task> next)
    {
        Console.WriteLine($"Selected service id: '{context.Arguments.ExecutionSettings?.FirstOrDefault().Key}'");
        Console.Write("Assistant > ");
        return next(context);
    }
}

class CustomRouter()
{
    /// <summary>
    /// Returns the best service id to use based on the user's input.
    /// This demonstration uses a simple logic where your input is checked for specific keywords as a deciding factor,
    /// if no keyword is found it defaults to the first service in the list.
    /// </summary>
    /// <param name="lookupPrompt">User's input prompt</param>
    /// <param name="serviceIds">List of service ids to choose from in order of importance, defaulting to the first</param>
    /// <returns>Service id.</returns>
    internal string GetService(string lookupPrompt, List<string> serviceIds)
    {
        // The order matters, if the keyword is not found, the first one is used.
        foreach (var serviceId in serviceIds)
        {
            if (Contains(lookupPrompt, serviceId))
            {
                return serviceId;
            }
        }

        return serviceIds[0];
    }

    // Ensure compatibility with both netstandard2.0 and net8.0 by using IndexOf instead of Contains
    private static bool Contains(string prompt, string pattern)
        => prompt.IndexOf(pattern, StringComparison.CurrentCultureIgnoreCase) >= 0;
}