using Microsoft.EntityFrameworkCore;
using DotnetApi.Data;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("Default")));

builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

// Sans condition Environment, Swagger est toujours actif (pratique en dev/docker)
app.UseSwagger();
app.UseSwaggerUI();

app.MapControllers();

app.Run();