using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Microsoft.IdentityModel.Tokens;
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;
using DotnetApi.Data;
using DotnetApi.Models;

// -------------------------------------------------------
// DTOs
// -------------------------------------------------------
public record RegisterRequest(string Nom, string Prenom, string Email, string Password);
public record LoginRequest(string Email, string Password);

// -------------------------------------------------------
// Controller Auth (pas de [Authorize] : routes publiques)
// -------------------------------------------------------
[ApiController]
[Route("auth")]
[Tags("Authentification")]
public class AuthController : ControllerBase
{
    private readonly AppDbContext _db;
    private readonly IConfiguration _config;

    public AuthController(AppDbContext db, IConfiguration config)
    {
        _db = db;
        _config = config;
    }

    // -------------------------------------------------------
    // POST /auth/register
    // -------------------------------------------------------
    [HttpPost("register")]
    public async Task<IActionResult> Register(RegisterRequest req)
    {
        // Vérifier si l'email est déjà utilisé
        var exists = await _db.Utilisateurs.AnyAsync(u => u.Email == req.Email);
        if (exists)
            return BadRequest(new { detail = "Email déjà utilisé!" });

        // Vérifier la longueur du mot de passe (limite bcrypt)
        if (System.Text.Encoding.UTF8.GetByteCount(req.Password) > 72)
            return BadRequest(new { detail = "Mot de passe trop long! (max 72 caractères pour bcrypt)" });

        // Hash du mot de passe avec BCrypt (compatible avec Python)
        var hashed = BCrypt.Net.BCrypt.HashPassword(req.Password);

        var user = new Utilisateur
        {
            Nom = req.Nom,
            Prenom = req.Prenom,
            Email = req.Email,
            Password = hashed
        };

        _db.Utilisateurs.Add(user);
        await _db.SaveChangesAsync();

        return StatusCode(201, new { message = "Utilisateur créé avec succès!", email = user.Email });
    }

    // -------------------------------------------------------
    // POST /auth/login  →  token JWT
    // -------------------------------------------------------
    [HttpPost("login")]
    public async Task<IActionResult> Login(LoginRequest req)
    {
        var user = await _db.Utilisateurs.FirstOrDefaultAsync(u => u.Email == req.Email);

        if (user == null)
            return Unauthorized(new { detail = "Email utilisateur incorrect" });

        if (!BCrypt.Net.BCrypt.Verify(req.Password, user.Password.Trim()))
            return Unauthorized(new { detail = "Mot de passe invalide" });

        var token = GenerateToken(user.Email);

        return Ok(new
        {
            access_token = token,
            token_type = "bearer",
            email = user.Email
        });
    }

    // -------------------------------------------------------
    // Génération du token JWT (même format que Python)
    // -------------------------------------------------------
    private string GenerateToken(string email)
    {
        var secretKey = _config["SECRET_KEY"] ?? _config["Jwt:SecretKey"]!;
        var expireMinutes = int.TryParse(_config["ACCESS_TOKEN_EXPIRE_MINUTES"], out var m) ? m : 60;

        var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(secretKey));
        var creds = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);

        // Claim "sub" = même clé que Python (create_access_token stocke sous "sub")
        var claims = new[] { new Claim("sub", email) };

        var token = new JwtSecurityToken(
            claims: claims,
            expires: DateTime.UtcNow.AddMinutes(expireMinutes),
            signingCredentials: creds
        );

        return new JwtSecurityTokenHandler().WriteToken(token);
    }
}
