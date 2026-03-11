using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using DotnetApi.Data;
using DotnetApi.Models;

[ApiController]
[Route("inscriptions")]
public class InscriptionsController : ControllerBase
{
    private readonly AppDbContext _db;
    public InscriptionsController(AppDbContext db){_db = db;}


    [HttpGet]
    public async Task<IActionResult> GetAll()
        => Ok(await _db.Inscrire.ToListAsync());


    [HttpPost]
    public async Task<IActionResult> Create(Inscrire link)
    {
        _db.Inscrire.Add(link);
        await _db.SaveChangesAsync();
        return StatusCode(201, link);
    }


    [HttpDelete("{idUtilisateur}/{idSession}")]
    public async Task<IActionResult> Delete(int idUtilisateur, int idSession)
    {
        var link = await _db.Inscrire
            .FirstOrDefaultAsync(x =>
                x.IdUtilisateur == idUtilisateur &&
                x.IdSession == idSession);

        if (link == null) return NotFound();

        _db.Inscrire.Remove(link);
        await _db.SaveChangesAsync();
        return NoContent();
    }
}