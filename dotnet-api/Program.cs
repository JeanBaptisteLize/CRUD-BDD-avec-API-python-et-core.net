using Microsoft.EntityFrameworkCore;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.IdentityModel.Tokens;
using Microsoft.OpenApi.Models;
using System.Text;
using DotnetApi.Data;

var builder = WebApplication.CreateBuilder(args);

// -------------------------------------------------------
// DB
// -------------------------------------------------------
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("Default")));

// -------------------------------------------------------
// JWT Authentication (même SECRET_KEY que l'API Python)
// -------------------------------------------------------
// SECRET_KEY lu depuis le .env (injecté par Docker Compose via env_file)
// Fallback sur appsettings.json si on tourne en dehors de Docker
var secretKey = builder.Configuration["SECRET_KEY"]          // lu depuis le .env via Docker
               ?? builder.Configuration["Jwt:SecretKey"]      // fallback appsettings.json
               ?? throw new InvalidOperationException("SECRET_KEY manquante");


builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuerSigningKey = true,
            IssuerSigningKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(secretKey)),
            ValidateIssuer = false,   // pas d'issuer défini côté Python
            ValidateAudience = false, // pas d'audience définie côté Python
            ValidateLifetime = true,  // vérifie l'expiration du token
        };
    });

builder.Services.AddAuthorization();

// -------------------------------------------------------
// Controllers + Swagger avec bouton Bearer
// -------------------------------------------------------
builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(options =>
{
    options.AddSecurityDefinition("Bearer", new OpenApiSecurityScheme
    {
        Name = "Authorization",
        Type = SecuritySchemeType.Http,
        Scheme = "bearer",
        BearerFormat = "JWT",
        In = ParameterLocation.Header,
        Description = "Entrez votre token JWT (sans le préfixe 'Bearer')"
    });

    // Cadenas uniquement sur les endpoints [Authorize], pas sur /auth/*
    options.OperationFilter<AuthorizeOperationFilter>();
});

var app = builder.Build();

// Sans condition Environment, Swagger est toujours actif (pratique en dev/docker)
app.UseSwagger();
app.UseSwaggerUI();

app.UseAuthentication();
app.UseAuthorization();

app.MapControllers();

app.Run();
