using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Authorization;
using Microsoft.EntityFrameworkCore;
using DotnetApi.Data;
using DotnetApi.Models;

[Authorize]
[ApiController]
[Route("resultats")]
public class ResultatsController : ControllerBase
{
    private readonly AppDbContext _db;
    public ResultatsController(AppDbContext db) { _db = db; }

    [HttpGet]
    public async Task<IActionResult> GetAll()
        => Ok(await _db.Resultats.ToListAsync());

    [HttpGet("{id}")]
    public async Task<IActionResult> Get(int id)
    {
        var obj = await _db.Resultats.FindAsync(id);
        if (obj == null) return NotFound(new { message = "Résultat non trouvé" });
        return Ok(obj);
    }

    [HttpPost]
    public async Task<IActionResult> Create(Resultat obj)
    {
        _db.Resultats.Add(obj);
        await _db.SaveChangesAsync();
        return StatusCode(201, new { message = "Résultat créé avec succès!", resultat = obj });
    }

    [HttpPut("{id}")]
    public async Task<IActionResult> Update(int id, Resultat payload)
    {
        var obj = await _db.Resultats.FindAsync(id);
        if (obj == null) return NotFound(new { message = "Résultat non trouvé" });

        obj.IdModule = payload.IdModule;
        obj.Note = payload.Note;
        obj.Reussite = payload.Reussite;
        obj.DatePassage = payload.DatePassage;
        obj.Tentative = payload.Tentative;

        await _db.SaveChangesAsync();
        return Ok(new { message = "Résultat mis à jour avec succès!", resultat = obj });
    }

    [HttpDelete("{id}")]
    public async Task<IActionResult> Delete(int id)
    {
        var obj = await _db.Resultats.FindAsync(id);
        if (obj == null) return NotFound(new { message = "Résultat non trouvé" });

        _db.Resultats.Remove(obj);
        await _db.SaveChangesAsync();
        return Ok(new { message = "Résultat supprimé avec succès!" });
    }
}
