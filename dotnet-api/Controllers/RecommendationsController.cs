using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Authorization;
using Microsoft.EntityFrameworkCore;
using DotnetApi.Data;
using DotnetApi.Models;

[Authorize]
[ApiController]
[Route("recommandations")]
public class RecommendationsController : ControllerBase
{
    private readonly AppDbContext _db;
    public RecommendationsController(AppDbContext db) { _db = db; }

    [HttpGet]
    public async Task<IActionResult> GetAll()
        => Ok(await _db.Recommandations.ToListAsync());

    [HttpGet("{id}")]
    public async Task<IActionResult> Get(int id)
    {
        var obj = await _db.Recommandations.FindAsync(id);
        if (obj == null) return NotFound(new { message = "Recommandation non trouvée" });
        return Ok(obj);
    }

    [HttpPost]
    public async Task<IActionResult> Create(RecommandationIA obj)
    {
        _db.Recommandations.Add(obj);
        await _db.SaveChangesAsync();
        return StatusCode(201, new { message = "Recommandation créée avec succès!", recommandation = obj });
    }

    [HttpPut("{id}")]
    public async Task<IActionResult> Update(int id, RecommandationIA payload)
    {
        var obj = await _db.Recommandations.FindAsync(id);
        if (obj == null) return NotFound(new { message = "Recommandation non trouvée" });

        obj.DateReco = payload.DateReco;
        obj.ScorePertinence = payload.ScorePertinence;
        obj.Motif = payload.Motif;

        await _db.SaveChangesAsync();
        return Ok(new { message = "Recommandation mise à jour avec succès!", recommandation = obj });
    }

    [HttpDelete("{id}")]
    public async Task<IActionResult> Delete(int id)
    {
        var obj = await _db.Recommandations.FindAsync(id);
        if (obj == null) return NotFound(new { message = "Recommandation non trouvée" });

        _db.Recommandations.Remove(obj);
        await _db.SaveChangesAsync();
        return Ok(new { message = "Recommandation supprimée avec succès!" });
    }
}
