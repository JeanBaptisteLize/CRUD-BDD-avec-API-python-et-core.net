using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace DotnetApi.Models;

[Table("Resultats")]
public class Resultat
{
    [Key]
    [Column("id_resultats")]
    public int IdResultats { get; set; }

    [Column("id_module")]
    public int IdModule { get; set; }

    [Column("note")]
    public int? Note { get; set; }

    [Column("reussite")]
    public byte? Reussite { get; set; }

    [Column("date_passage")]
    public string DatePassage { get; set; } = string.Empty;

    [Column("tentative")]
    public byte? Tentative { get; set; }
}