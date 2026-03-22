using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Authorization;
using Microsoft.EntityFrameworkCore;
using DotnetApi.Data;
using DotnetApi.Models;

[Authorize]
[ApiController]
[Route("formations")]
public class FormationsController : ControllerBase
{
    private readonly AppDbContext _db;
    public FormationsController(AppDbContext db) { _db = db; }

    [HttpGet]
    public async Task<IActionResult> GetAll()
        => Ok(await _db.Formations.ToListAsync());

    [HttpGet("{id}")]
    public async Task<IActionResult> Get(int id)
    {
        var obj = await _db.Formations.FindAsync(id);
        if (obj == null) return NotFound(new { message = "Formation non trouvée" });
        return Ok(obj);
    }

    [HttpPost]
    public async Task<IActionResult> Create(Formation obj)
    {
        _db.Formations.Add(obj);
        await _db.SaveChangesAsync();
        return StatusCode(201, new { message = "Formation créée avec succès!", formation = obj });
    }

    [HttpPut("{id}")]
    public async Task<IActionResult> Update(int id, Formation payload)
    {
        var obj = await _db.Formations.FindAsync(id);
        if (obj == null) return NotFound(new { message = "Formation non trouvée" });

        obj.Titre = payload.Titre;
        obj.Description = payload.Description;
        obj.Duree = payload.Duree;

        await _db.SaveChangesAsync();
        return Ok(new { message = "Formation mise à jour avec succès!", formation = obj });
    }

    [HttpDelete("{id}")]
    public async Task<IActionResult> Delete(int id)
    {
        var obj = await _db.Formations.FindAsync(id);
        if (obj == null) return NotFound(new { message = "Formation non trouvée" });

        _db.Formations.Remove(obj);
        await _db.SaveChangesAsync();
        return Ok(new { message = "Formation supprimée avec succès!" });
    }
}
