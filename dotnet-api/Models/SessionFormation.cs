using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace DotnetApi.Models;

[Table("SessionFormations")]
public class SessionFormation
{
    [Key]
    [Column("id_session")]
    public int IdSession { get; set; }

    [Column("id_formation")]
    public int IdFormation { get; set; }

    [Column("date_debut")]
    public string DateDebut { get; set; } = string.Empty;

    [Column("date_fin")]
    public string DateFin { get; set; } = string.Empty;

    [Column("lieu")]
    public string Lieu { get; set; } = string.Empty;

    [Column("capacite")]
    public int Capacite { get; set; }

    [Column("mode_presentiel")]
    public byte? ModePresentiel { get; set; }
}