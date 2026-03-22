using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Authorization;
using Microsoft.EntityFrameworkCore;
using DotnetApi.Data;
using DotnetApi.Models;

[Authorize]
[ApiController]
[Route("obtenir")]
public class ObtenirController : ControllerBase
{
    private readonly AppDbContext _db;
    public ObtenirController(AppDbContext db) { _db = db; }

    [HttpGet]
    public async Task<IActionResult> GetAll()
        => Ok(await _db.Obtenir.ToListAsync());

    [HttpPost]
    public async Task<IActionResult> Create(Obtenir obj)
    {
        _db.Obtenir.Add(obj);
        await _db.SaveChangesAsync();
        return StatusCode(201, new { message = "Lien utilisateur-résultat (obtenir) créé avec succès!", lien = obj });
    }

    [HttpDelete("{idUtilisateur}/{idResultats}")]
    public async Task<IActionResult> Delete(int idUtilisateur, int idResultats)
    {
        var obj = await _db.Obtenir.FirstOrDefaultAsync(x =>
            x.IdUtilisateur == idUtilisateur && x.IdResultats == idResultats);
        if (obj == null) return NotFound(new { message = "Lien utilisateur-résultat non trouvé" });

        _db.Obtenir.Remove(obj);
        await _db.SaveChangesAsync();
        return Ok(new { message = "Lien utilisateur-résultat (obtenir) supprimé avec succès!" });
    }
}
