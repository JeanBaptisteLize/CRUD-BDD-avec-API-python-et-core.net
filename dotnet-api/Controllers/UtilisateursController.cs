using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using DotnetApi.Data;
using DotnetApi.Models;

[ApiController]
[Route("utilisateurs")]
public class UtilisateursController : ControllerBase
{
    private readonly AppDbContext _db;
    public UtilisateursController(AppDbContext db){_db = db;}


    [HttpGet]
    public async Task<IActionResult> GetAll()
        => Ok(await _db.Utilisateurs.ToListAsync());


    [HttpGet("{id}")]
    public async Task<IActionResult> Get(int id)
    {
        var obj = await _db.Utilisateurs.FindAsync(id);
        return obj == null ? NotFound() : Ok(obj);
    }


    [HttpPost]
    public async Task<IActionResult> Create(Utilisateur obj)
    {
        _db.Utilisateurs.Add(obj);
        await _db.SaveChangesAsync();
        return CreatedAtAction(nameof(Get), new { id = obj.IdUtilisateur }, obj);
    }


    [HttpPut("{id}")]
    public async Task<IActionResult> Update(int id, Utilisateur payload)
    {
        var obj = await _db.Utilisateurs.FindAsync(id);
        if (obj == null) return NotFound();

        obj.Nom = payload.Nom;
        obj.Prenom = payload.Prenom;
        obj.Email = payload.Email;

        await _db.SaveChangesAsync();
        return Ok(obj);
    }

    [HttpDelete("{id}")]
    public async Task<IActionResult> Delete(int id)
    {
        var obj = await _db.Utilisateurs.FindAsync(id);
        if (obj == null) return NotFound();

        _db.Utilisateurs.Remove(obj);
        await _db.SaveChangesAsync();
        return NoContent();
    }
}