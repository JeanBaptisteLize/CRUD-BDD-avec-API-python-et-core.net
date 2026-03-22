using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Authorization;
using Microsoft.EntityFrameworkCore;
using DotnetApi.Data;
using DotnetApi.Models;

[Authorize]
[ApiController]
[Route("recommander")]
public class RecommanderController : ControllerBase
{
    private readonly AppDbContext _db;
    public RecommanderController(AppDbContext db) { _db = db; }

    [HttpGet]
    public async Task<IActionResult> GetAll()
        => Ok(await _db.Recommander.ToListAsync());

    [HttpPost]
    public async Task<IActionResult> Create(Recommander obj)
    {
        _db.Recommander.Add(obj);
        await _db.SaveChangesAsync();
        return StatusCode(201, new { message = "Lien utilisateur-recommandation créé avec succès!", lien = obj });
    }

    [HttpDelete("{idUtilisateur}/{idRecommandation}")]
    public async Task<IActionResult> Delete(int idUtilisateur, int idRecommandation)
    {
        var obj = await _db.Recommander.FirstOrDefaultAsync(x =>
            x.IdUtilisateur == idUtilisateur && x.IdRecommandation == idRecommandation);
        if (obj == null) return NotFound(new { message = "Lien utilisateur-recommandation non trouvé" });

        _db.Recommander.Remove(obj);
        await _db.SaveChangesAsync();
        return Ok(new { message = "Lien utilisateur-recommandation supprimé avec succès!" });
    }
}
