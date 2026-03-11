using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace DotnetApi.Models;

[Table("Formations")]
public class Formation
{
    [Key]
    [Column("id_formation")]
    public int IdFormation { get; set; }

    [Column("titre")]
    public string Titre { get; set; } = string.Empty;

    [Column("description")]
    public string Description { get; set; } = string.Empty;

    [Column("duree")]
    public string? Duree { get; set; }
}