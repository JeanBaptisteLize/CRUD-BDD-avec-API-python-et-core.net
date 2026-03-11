using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace DotnetApi.Models;

[Table("ModulesFormations")]
public class ModuleFormation
{
    [Key]
    [Column("id_module")]
    public int IdModule { get; set; }

    [Column("titre")]
    public string Titre { get; set; } = string.Empty;

    [Column("contenu")]
    public string Contenu { get; set; } = string.Empty;

    [Column("duree")]
    public string? Duree { get; set; }
}