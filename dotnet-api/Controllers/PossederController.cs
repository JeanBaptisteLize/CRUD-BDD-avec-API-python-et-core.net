using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Authorization;
using Microsoft.EntityFrameworkCore;
using DotnetApi.Data;
using DotnetApi.Models;

[Authorize]
[ApiController]
[Route("posseder")]
public class PossederController : ControllerBase
{
    private readonly AppDbContext _db;
    public PossederController(AppDbContext db) { _db = db; }

    [HttpGet]
    public async Task<IActionResult> GetAll()
        => Ok(await _db.Posseder.ToListAsync());

    [HttpPost]
    public async Task<IActionResult> Create(Posseder obj)
    {
        _db.Posseder.Add(obj);
        await _db.SaveChangesAsync();
        return StatusCode(201, new { message = "Lien module-formation créé avec succès!", lien = obj });
    }

    [HttpDelete("{idModule}/{idFormation}")]
    public async Task<IActionResult> Delete(int idModule, int idFormation)
    {
        var obj = await _db.Posseder.FirstOrDefaultAsync(x =>
            x.IdModule == idModule && x.IdFormation == idFormation);
        if (obj == null) return NotFound(new { message = "Lien module-formation non trouvé" });

        _db.Posseder.Remove(obj);
        await _db.SaveChangesAsync();
        return Ok(new { message = "Lien module-formation supprimé avec succès!" });
    }
}
