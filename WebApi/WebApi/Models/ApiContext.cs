using Microsoft.EntityFrameworkCore;

namespace WebApi.Models{
    public class ApiContext : DbContext{
        public ApiContext(DbContextOptions<ApiContext> options):base(options){}

        public DbSet<Data> dane {get; set;} 
        public DbSet<Session> sesja {get; set;} 

    }
}