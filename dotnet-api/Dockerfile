# Build : on compile le projet dans un conteneur SDK (Software Developement Kit) notre première image
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

# On copie le fichier projet avec son nom explicite
COPY DotnetApi.csproj .
RUN dotnet restore

# On copie tout le reste et on compile
COPY . .
RUN dotnet publish -c Release -o /app/publish

# Runtime : on obtient une image plus légère, juste pour exécuter
FROM mcr.microsoft.com/dotnet/aspnet:8.0
WORKDIR /app
COPY --from=build /app/publish .

# On remplace le DotnetApi.dll par le nom du projet dans le fichier .csproj
ENTRYPOINT ["dotnet", "DotnetApi.dll"]