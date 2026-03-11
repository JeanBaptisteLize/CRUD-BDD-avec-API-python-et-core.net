using System.ComponentModel.DataAnnotations.Schema;

namespace DotnetApi.Models;

[Table("Posseder")]
public class Posseder
{
    [Column("id_module")]    public int IdModule { get; set; }
    [Column("id_formation")] public int IdFormation { get; set; }
}

[Table("Suggerer")] 
public class Suggerer
{
    [Column("id_recommandation")] public int IdRecommandation { get; set; }
    [Column("id_formation")]      public int IdFormation { get; set; }
}

[Table("Recommander")]
public class Recommander
{
    [Column("id_utilisateur")]    public int IdUtilisateur { get; set; }
    [Column("id_recommandation")] public int IdRecommandation { get; set; }
}

[Table("Inscrire")]
public class Inscrire
{
    [Column("id_utilisateur")] public int IdUtilisateur { get; set; }
    [Column("id_session")]     public int IdSession { get; set; }
    [Column("date_inscription")] public string DateInscription { get; set; } = string.Empty;
}

[Table("Obtenir")]
public class Obtenir
{
    [Column("id_utilisateur")] public int IdUtilisateur { get; set; }
    [Column("id_resultats")]   public int IdResultats { get; set; }
}

[Table("Passer")]
public class Passer
{
    [Column("id_utilisateur")] public int IdUtilisateur { get; set; }
    [Column("id_resultats")]   public int IdResultats { get; set; }
}