using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Authorization;
using Microsoft.EntityFrameworkCore;
using DotnetApi.Data;
using DotnetApi.Models;

[Authorize]
[ApiController]
[Route("utilisateurs")]
public class UtilisateursController : ControllerBase
{
    private readonly AppDbContext _db;
    public UtilisateursController(AppDbContext db) { _db = db; }


    [HttpGet]
    public async Task<IActionResult> GetAll()
        => Ok(await _db.Utilisateurs.ToListAsync());


    [HttpGet("{id}")]
    public async Task<IActionResult> Get(int id)
    {
        var obj = await _db.Utilisateurs.FindAsync(id);
        if (obj == null) return NotFound(new { message = "Utilisateur non trouvé" });
        return Ok(obj);
    }


    [HttpPost]
    public async Task<IActionResult> Create(Utilisateur obj)
    {
        _db.Utilisateurs.Add(obj);
        await _db.SaveChangesAsync();
        return StatusCode(201, new { message = "Utilisateur créé avec succès!", utilisateur = obj });
    }


    [HttpPut("{id}")]
    public async Task<IActionResult> Update(int id, Utilisateur payload)
    {
        var obj = await _db.Utilisateurs.FindAsync(id);
        if (obj == null) return NotFound(new { message = "Utilisateur non trouvé" });

        obj.Nom = payload.Nom;
        obj.Prenom = payload.Prenom;
        obj.Email = payload.Email;

        await _db.SaveChangesAsync();
        return Ok(new { message = "Utilisateur mis à jour avec succès!", utilisateur = obj });
    }


    [HttpDelete("{id}")]
    public async Task<IActionResult> Delete(int id)
    {
        var obj = await _db.Utilisateurs.FindAsync(id);
        if (obj == null) return NotFound(new { message = "Utilisateur non trouvé" });

        _db.Utilisateurs.Remove(obj);
        await _db.SaveChangesAsync();
        return Ok(new { message = "Utilisateur supprimé avec succès!" });
    }
}
