using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Authorization;
using Microsoft.EntityFrameworkCore;
using DotnetApi.Data;
using DotnetApi.Models;

[Authorize]
[ApiController]
[Route("modules")]
public class ModulesController : ControllerBase
{
    private readonly AppDbContext _db;
    public ModulesController(AppDbContext db) { _db = db; }

    [HttpGet]
    public async Task<IActionResult> GetAll()
        => Ok(await _db.Modules.ToListAsync());

    [HttpGet("{id}")]
    public async Task<IActionResult> Get(int id)
    {
        var obj = await _db.Modules.FindAsync(id);
        if (obj == null) return NotFound(new { message = "Module non trouvé" });
        return Ok(obj);
    }

    [HttpPost]
    public async Task<IActionResult> Create(ModuleFormation obj)
    {
        _db.Modules.Add(obj);
        await _db.SaveChangesAsync();
        return StatusCode(201, new { message = "Module créé avec succès!", module = obj });
    }

    [HttpPut("{id}")]
    public async Task<IActionResult> Update(int id, ModuleFormation payload)
    {
        var obj = await _db.Modules.FindAsync(id);
        if (obj == null) return NotFound(new { message = "Module non trouvé" });

        obj.Titre = payload.Titre;
        obj.Contenu = payload.Contenu;
        obj.Duree = payload.Duree;

        await _db.SaveChangesAsync();
        return Ok(new { message = "Module mis à jour avec succès!", module = obj });
    }

    [HttpDelete("{id}")]
    public async Task<IActionResult> Delete(int id)
    {
        var obj = await _db.Modules.FindAsync(id);
        if (obj == null) return NotFound(new { message = "Module non trouvé" });

        _db.Modules.Remove(obj);
        await _db.SaveChangesAsync();
        return Ok(new { message = "Module supprimé avec succès!" });
    }
}
