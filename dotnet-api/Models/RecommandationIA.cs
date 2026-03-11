using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace DotnetApi.Models;

[Table("RecommandationsIA")]
public class RecommandationIA
{
    [Key]
    [Column("id_recommandation")]
    public int IdRecommandation { get; set; }

    [Column("date_reco")]
    public string DateReco { get; set; } = string.Empty;

    [Column("score_pertinence")]
    public int ScorePertinence { get; set; }

    [Column("motif")]
    public string? Motif { get; set; }
}