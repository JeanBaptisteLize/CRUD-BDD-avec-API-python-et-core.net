using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace DotnetApi.Models;

[Table("Utilisateurs")]         // nom exacte de la table dans FormationDB
public class Utilisateur
{
    [Key]
    [Column("id_utilisateur")]
    public int IdUtilisateur { get; set; }

    [Column("nom")]
    public string Nom { get; set; } = string.Empty;

    [Column("prenom")]
    public string Prenom { get; set; } = string.Empty;

    [Column("email")]
    public string Email { get; set; } = string.Empty;

    [Column("password")]
    public string Password { get; set; } = string.Empty;    // stock le hashé
}