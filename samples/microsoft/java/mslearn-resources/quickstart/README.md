# Java QuickStart for Azure AI Foundry SDK

This quickstart guide demonstrates how to use the Azure AI Foundry SDK with Java to create projects, run chat completions, create agents, add file search capabilities, and evaluate agent runs.

## Prerequisites

- Java Development Kit (JDK) 17 or later
    - We recommend the [Microsoft Build of OpenJDK](https://learn.microsoft.com/en-us/java/openjdk/download), which is a free, Long-Term Support (LTS) distribution of OpenJDK
- Maven 3.6.0 or later
    - Download from the [Apache Maven website](https://maven.apache.org/download.cgi)
- An Azure subscription with access to Azure AI services
    - Free account: [Create an Azure account](https://azure.microsoft.com/free/)
- Access to [Azure AI Foundry](https://ai.azure.com)
- Install the [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)

## Setup

### Development Environment

#### Visual Studio Code Setup (Recommended)

1. **Install Visual Studio Code**
   - Download and install from [VS Code website](https://code.visualstudio.com/)

2. **Install Java Extensions**
   - Install the [Extension Pack for Java](https://marketplace.visualstudio.com/items?itemName=vscjava.vscode-java-pack) which includes:
     - Language Support for Java by Red Hat
     - Debugger for Java
     - Test Runner for Java
     - Maven for Java
     - Project Manager for Java
     - Visual Studio IntelliCode
   
3. **Configure Java in VS Code**
   - Set JAVA_HOME environment variable pointing to your JDK installation
   - Follow the [VS Code Java setup guide](https://code.visualstudio.com/docs/languages/java) for detailed instructions

4. **Install Additional Helpful Extensions**
   - [Azure Tools](https://marketplace.visualstudio.com/items?itemName=ms-vscode.vscode-node-azure-pack) for Azure integration
   - [GitHub Pull Requests](https://marketplace.visualstudio.com/items?itemName=GitHub.vscode-pull-request-github) for GitHub integration

#### Other IDEs
You can also use other IDEs such as:
- [IntelliJ IDEA](https://www.jetbrains.com/idea/) (Community or Ultimate edition)
- [Eclipse](https://www.eclipse.org/downloads/) with the Maven plugin

### Rename .env.template to .env

Rename the `.env.template` file to `.env` and fill in your Azure credentials:

```properties
AZURE_API_KEY=your_api_key_here
AZURE_ENDPOINT=your_endpoint_here
AZURE_DEPLOYMENT=your_deployment_name_here
```

### Install Dependencies

1. Install the [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)
2. Log in to Azure:
   ```bash
   az login
   ```
3. Add Maven dependencies:

```xml
    <dependencies>
        <dependency>
            <groupId>com.azure</groupId>
            <artifactId>azure-ai-projects</artifactId>
            <version>1.0.0-alpha.20250429.2</version>
        </dependency>
        
        <!-- OpenAI Java SDK -->
        <dependency>
            <groupId>com.openai</groupId>
            <artifactId>openai-java</artifactId>
            <version>1.4.1</version>
        </dependency>
        
        <!-- Azure Identity for authentication -->
        <dependency>
            <groupId>com.azure</groupId>
            <artifactId>azure-identity</artifactId>
            <version>1.8.1</version>
        </dependency>
        
        <!-- .env file support -->
        <dependency>
            <groupId>io.github.cdimascio</groupId>
            <artifactId>dotenv-java</artifactId>
            <version>2.3.2</version>
        </dependency>
        
        <!-- Logging -->
        <dependency>
            <groupId>org.slf4j</groupId>
            <artifactId>slf4j-api</artifactId>
            <version>2.0.7</version>
        </dependency>
        <dependency>
            <groupId>org.slf4j</groupId>
            <artifactId>slf4j-simple</artifactId>
            <version>2.0.7</version>
        </dependency>
    </dependencies>
```

## Create a Project and Model Deployment


```java
// Create a client using your Azure credentials
ProjectsClient client = new ProjectsClientBuilder()
    .credential(new AzureKeyCredential(System.getenv("AZURE_API_KEY")))
    .endpoint(System.getenv("AZURE_ENDPOINT"))
    .buildClient();

// Create a project with a name and description
Project project = client.createProject("My Sample Project", "A project created using the Java SDK");
System.out.println("Created project: " + project.getName() + " with ID: " + project.getId());
```

## Chat Completion

```java
// Create a Projects client
ProjectsClient client = new ProjectsClientBuilder()
    .credential(new AzureKeyCredential(System.getenv("AZURE_API_KEY")))
    .endpoint(System.getenv("AZURE_ENDPOINT"))
    .buildClient();

// Get a chat client from the project
ChatClient chatClient = client.getChatClient(System.getenv("AZURE_DEPLOYMENT"));

// Create chat messages
List<ChatMessage> messages = Arrays.asList(
    new ChatMessage(ChatRole.SYSTEM, "You are a helpful assistant."),
    new ChatMessage(ChatRole.USER, "Tell me about Azure AI Foundry.")
);

// Get chat completion
ChatCompletionOptions options = new ChatCompletionOptions(messages)
    .setTemperature(0.7)
    .setMaxTokens(800);

ChatCompletion completion = chatClient.getChatCompletion(options);
System.out.println(completion.getChoices().get(0).getMessage().getContent());
```

## Create and Run an Agent


```java
// Create a Projects client
ProjectsClient client = new ProjectsClientBuilder()
    .credential(new AzureKeyCredential(System.getenv("AZURE_API_KEY")))
    .endpoint(System.getenv("AZURE_ENDPOINT"))
    .buildClient();

// Get an agent client
AgentClient agentClient = client.getAgentClient();

// Create an agent
Agent agent = agentClient.createAgent(new AgentOptions()
    .setName("Research Assistant")
    .setDescription("An agent that helps with research tasks")
    .setInstructions("You are a research assistant. Help users find information and summarize content.")
    .setModel(System.getenv("AZURE_DEPLOYMENT")));

// Run the agent with a task
AgentThread thread = agentClient.createThread();
AgentMessage userMessage = new AgentMessage()
    .setRole(AgentRole.USER)
    .setContent("Research the benefits of cloud computing");

AgentRun run = agentClient.createRun(thread.getId(), agent.getId(), userMessage);

// Wait for the run to complete and get the results
AgentMessage assistantMessage = agentClient.getMessages(thread.getId())
    .stream()
    .filter(message -> message.getRole() == AgentRole.ASSISTANT)
    .findFirst()
    .orElse(null);

if (assistantMessage != null) {
    System.out.println("Agent response: " + assistantMessage.getContent());
}
```

## Add File Search to Agent

Add file search capabilities to your agent:

```java
// Create a Projects client
ProjectsClient client = new ProjectsClientBuilder()
    .credential(new AzureKeyCredential(System.getenv("AZURE_API_KEY")))
    .endpoint(System.getenv("AZURE_ENDPOINT"))
    .buildClient();

// Get an agent client
AgentClient agentClient = client.getAgentClient();

// Upload a file for search
FileClient fileClient = client.getFileClient();
File uploadedFile = fileClient.uploadFile("path/to/your/document.pdf");

// Add file search capability to the agent
Agent agent = agentClient.createAgent(new AgentOptions()
    .setName("Document Assistant")
    .setDescription("An agent that helps with document searching")
    .setInstructions("You are a document assistant. Help users find information in their documents.")
    .setModel(System.getenv("AZURE_DEPLOYMENT"))
    .addTool(new FileTool()
        .addFile(uploadedFile.getId())));

// Run the agent with a file search query
AgentThread thread = agentClient.createThread();
AgentMessage userMessage = new AgentMessage()
    .setRole(AgentRole.USER)
    .setContent("Find information about cloud computing in my document");

AgentRun run = agentClient.createRun(thread.getId(), agent.getId(), userMessage);

// Display the search results
AgentMessage assistantMessage = agentClient.getMessages(thread.getId())
    .stream()
    .filter(message -> message.getRole() == AgentRole.ASSISTANT)
    .findFirst()
    .orElse(null);

if (assistantMessage != null) {
    System.out.println("Search results: " + assistantMessage.getContent());
}
```

## Evaluate Agent Run

Evaluate how well the agent performed on a given task:

```java
// Create a Projects client
ProjectsClient client = new ProjectsClientBuilder()
    .credential(new AzureKeyCredential(System.getenv("AZURE_API_KEY")))
    .endpoint(System.getenv("AZURE_ENDPOINT"))
    .buildClient();

// Get an evaluation client
EvaluationClient evaluationClient = client.getEvaluationClient();

// Create an evaluation for an agent run
AgentEvaluation evaluation = evaluationClient.evaluateAgentRun(
    "agent-run-id", 
    new EvaluationOptions()
        .addMetric(EvaluationMetric.HELPFULNESS)
        .addMetric(EvaluationMetric.ACCURACY)
);

// Display the evaluation results
System.out.println("Evaluation results:");
System.out.println("Helpfulness score: " + evaluation.getScores().get(EvaluationMetric.HELPFULNESS));
System.out.println("Accuracy score: " + evaluation.getScores().get(EvaluationMetric.ACCURACY));
```


