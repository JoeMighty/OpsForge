# Container Image Inspector

The **Container Image Inspector** analyzes Docker images to identify excessively large layers and retrieve detailed metadata. It helps developers and DevOps engineers optimize image sizes and understand the build history of a container.

## Syntax

```bash
opsforge cloud image-inspect [IMAGE_NAME]
```

### Arguments
- `IMAGE_NAME`: The name or ID of the local Docker image (e.g., `nginx:latest`).

## Usage Examples

### Inspect a local image
```bash
opsforge cloud image-inspect my-app:v1
```

## Data Extracted
- **Layer History**: Breaks down the image into its constituent layers, showing the size of each layer and the Dockerfile command (`CreatedBy`) that generated it.
- **Architecture/OS**: Displays the target CPU architecture (e.g., `amd64`) and operating system.
- **Author**: Shows the image author/maintainer if specified in the metadata.

## Technical Details
This tool acts as a wrapper around the `docker inspect` and `docker history` commands. It parses the resulting JSON and formatted output to provide a clean, readable summary in the terminal.

> [!IMPORTANT]
> **Prerequisites**: This tool requires the **Docker Desktop** or **Docker Engine** to be installed and running on the local system. The image must also be available locally (i.e., you must run `docker pull` first if the image is in a remote registry).

## Optimization Tips
- **Multi-stage builds**: Use multi-stage builds to keep the final image small by excluding build-time dependencies.
- **Combine RUN commands**: Combine multiple `apt-get` or `pip install` commands into a single `RUN` instruction to reduce the number of layers.
- **Clear Caches**: Always clear package manager caches (e.g., `rm -rf /var/lib/apt/lists/*`) in the same layer they were created.
