using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Authorization;
using Microsoft.EntityFrameworkCore;
using DotnetApi.Data;
using DotnetApi.Models;

[Authorize]
[ApiController]
[Route("passer")]
public class PasserController : ControllerBase
{
    private readonly AppDbContext _db;
    public PasserController(AppDbContext db) { _db = db; }

    [HttpGet]
    public async Task<IActionResult> GetAll()
        => Ok(await _db.Passer.ToListAsync());

    [HttpPost]
    public async Task<IActionResult> Create(Passer obj)
    {
        _db.Passer.Add(obj);
        await _db.SaveChangesAsync();
        return StatusCode(201, new { message = "Lien utilisateur-résultat (passer) créé avec succès!", lien = obj });
    }

    [HttpDelete("{idUtilisateur}/{idResultats}")]
    public async Task<IActionResult> Delete(int idUtilisateur, int idResultats)
    {
        var obj = await _db.Passer.FirstOrDefaultAsync(x =>
            x.IdUtilisateur == idUtilisateur && x.IdResultats == idResultats);
        if (obj == null) return NotFound(new { message = "Lien utilisateur-résultat non trouvé" });

        _db.Passer.Remove(obj);
        await _db.SaveChangesAsync();
        return Ok(new { message = "Lien utilisateur-résultat (passer) supprimé avec succès!" });
    }
}
