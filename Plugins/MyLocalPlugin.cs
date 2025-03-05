using System.ComponentModel;
using Microsoft.SemanticKernel;

public class MyLocalPlugin
{
    [KernelFunction, Description("Get the current time")]
    public DateTimeOffset Time() => DateTimeOffset.Now;
}