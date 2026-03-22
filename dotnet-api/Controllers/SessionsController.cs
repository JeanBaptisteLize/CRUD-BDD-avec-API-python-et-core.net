using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Authorization;
using Microsoft.EntityFrameworkCore;
using DotnetApi.Data;
using DotnetApi.Models;

[Authorize]
[ApiController]
[Route("sessions")]
public class SessionsController : ControllerBase
{
    private readonly AppDbContext _db;
    public SessionsController(AppDbContext db) { _db = db; }

    [HttpGet]
    public async Task<IActionResult> GetAll()
        => Ok(await _db.Sessions.ToListAsync());

    [HttpGet("{id}")]
    public async Task<IActionResult> Get(int id)
    {
        var obj = await _db.Sessions.FindAsync(id);
        if (obj == null) return NotFound(new { message = "Session non trouvée" });
        return Ok(obj);
    }

    [HttpPost]
    public async Task<IActionResult> Create(SessionFormation obj)
    {
        _db.Sessions.Add(obj);
        await _db.SaveChangesAsync();
        return StatusCode(201, new { message = "Session créée avec succès!", session = obj });
    }

    [HttpPut("{id}")]
    public async Task<IActionResult> Update(int id, SessionFormation payload)
    {
        var obj = await _db.Sessions.FindAsync(id);
        if (obj == null) return NotFound(new { message = "Session non trouvée" });

        obj.IdFormation = payload.IdFormation;
        obj.DateDebut = payload.DateDebut;
        obj.DateFin = payload.DateFin;
        obj.Lieu = payload.Lieu;
        obj.Capacite = payload.Capacite;
        obj.ModePresentiel = payload.ModePresentiel;

        await _db.SaveChangesAsync();
        return Ok(new { message = "Session mise à jour avec succès!", session = obj });
    }

    [HttpDelete("{id}")]
    public async Task<IActionResult> Delete(int id)
    {
        var obj = await _db.Sessions.FindAsync(id);
        if (obj == null) return NotFound(new { message = "Session non trouvée" });

        _db.Sessions.Remove(obj);
        await _db.SaveChangesAsync();
        return Ok(new { message = "Session supprimée avec succès!" });
    }
}
