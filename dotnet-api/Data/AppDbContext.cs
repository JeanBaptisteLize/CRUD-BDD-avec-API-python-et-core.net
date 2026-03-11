using Microsoft.EntityFrameworkCore;
using DotnetApi.Models;

namespace DotnetApi.Data
{
    public class AppDbContext : DbContext
    {
        public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) {}

        public DbSet<Utilisateur>       Utilisateurs    { get; set; }
        public DbSet<Formation>         Formations      { get; set; }
        public DbSet<ModuleFormation>   Modules         { get; set; }
        public DbSet<SessionFormation>  Sessions        { get; set; }
        public DbSet<Resultat>          Resultats       { get; set; }
        public DbSet<RecommandationIA>  Recommandations { get; set; }

        public DbSet<Posseder>      Posseder    { get; set; }
        public DbSet<Suggerer>      Suggerer    { get; set; }
        public DbSet<Recommander>   Recommander { get; set; }
        public DbSet<Inscrire>      Inscrire    { get; set; }
        public DbSet<Obtenir>       Obtenir     { get; set; }
        public DbSet<Passer>        Passer      { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            // Clés composites pour les tables d'association
            modelBuilder.Entity<Posseder>()
                .HasKey(x => new { x.IdModule, x.IdFormation });

            modelBuilder.Entity<Suggerer>()
                .HasKey(x => new { x.IdRecommandation, x.IdFormation });

            modelBuilder.Entity<Recommander>()
                .HasKey(x => new { x.IdUtilisateur, x.IdRecommandation });

            modelBuilder.Entity<Inscrire>()
                .HasKey(x => new { x.IdUtilisateur, x.IdSession });

            modelBuilder.Entity<Obtenir>()
                .HasKey(x => new { x.IdUtilisateur, x.IdResultats });

            modelBuilder.Entity<Passer>()
                .HasKey(x => new { x.IdUtilisateur, x.IdResultats });
        }
    }
}