using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Authorization;
using Microsoft.EntityFrameworkCore;
using DotnetApi.Data;
using DotnetApi.Models;

[Authorize]
[ApiController]
[Route("suggere")]
public class SuggereController : ControllerBase
{
    private readonly AppDbContext _db;
    public SuggereController(AppDbContext db) { _db = db; }

    [HttpGet]
    public async Task<IActionResult> GetAll()
        => Ok(await _db.Suggerer.ToListAsync());

    [HttpPost]
    public async Task<IActionResult> Create(Suggerer obj)
    {
        _db.Suggerer.Add(obj);
        await _db.SaveChangesAsync();
        return StatusCode(201, new { message = "Lien recommandation-formation créé avec succès!", lien = obj });
    }

    [HttpDelete("{idRecommandation}/{idFormation}")]
    public async Task<IActionResult> Delete(int idRecommandation, int idFormation)
    {
        var obj = await _db.Suggerer.FirstOrDefaultAsync(x =>
            x.IdRecommandation == idRecommandation && x.IdFormation == idFormation);
        if (obj == null) return NotFound(new { message = "Lien recommandation-formation non trouvé" });

        _db.Suggerer.Remove(obj);
        await _db.SaveChangesAsync();
        return Ok(new { message = "Lien recommandation-formation supprimé avec succès!" });
    }
}
