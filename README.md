# sk-hybrid-console-cs

This project is a hybrid console application that integrates multiple AI services for chat completion using Microsoft Semantic Kernel. It supports both local and cloud-based AI models and allows for dynamic service selection based on user input.

## Project Structure

```
.env
.gitignore
bin/
obj/
Plugins/
    MyLocalPlugin.cs
    MyTimePlugin.cs
Program.cs
sk-hybrid-console-cs.csproj
sk-hybrid-console-cs.sln
```

## Prerequisites

- [.NET 9.0 SDK](https://dotnet.microsoft.com/download/dotnet/9.0)
- [Azure OpenAI Service](https://azure.microsoft.com/en-us/services/cognitive-services/openai-service/)
- [Ollama](https://ollama.com/)

## Setup

1. **Clone the repository:**

    ```sh
    git clone https://github.com/yourusername/sk-hybrid-console-cs.git
    cd sk-hybrid-console-cs
    ```

2. **Install dependencies:**

    ```sh
    dotnet restore
    ```

3. **Set up the .env file:**

    Create a .env file in the root directory of the project and add the following environment variables:

    ```env
    OPENAI_CHAT_MODEL_ID=your_openai_chat_model_id
    OPENAI_API_KEY=your_openai_api_key
    ```

4. **Build the project:**

    ```sh
    dotnet build
    ```

## Running the Application

To run the application, use the following command:

```sh
dotnet run
```

## Usage

The application will prompt you to enter text. Based on your input, it will route the request to either the local or cloud-based AI service and display the response.

## Adding Plugins

You can add custom plugins by creating new classes in the Plugins directory and registering them in Program.cs:

```csharp
kernel.Plugins.AddFromType<MyCustomPlugin>();
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## Contact

For any questions or feedback, please contact [yourname@yourdomain.com](mailto:yourname@yourdomain.com).

---

This README provides an overview of the project, setup instructions, and usage guidelines. Make sure to replace placeholders with your actual information.