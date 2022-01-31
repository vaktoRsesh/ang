using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using WebApi.Models;
using Microsoft.EntityFrameworkCore;

namespace WebApi
{
    public class Startup
    {
        private string _connectionString = null;
        public Startup(IConfiguration configuration)
        {
            Configuration = configuration;
        }

        public IConfiguration Configuration { get; }

        // This method gets called by the runtime. Use this method to add services to the container.
        public void ConfigureServices(IServiceCollection services)
        {
            services.AddCors(opt =>{
                opt.AddPolicy("CorsPolicy",
                c=> c.AllowAnyOrigin().AllowAnyHeader().AllowAnyMethod());
            });
            _connectionString = Configuration["secretConnectionString"];
            services.AddMvc();
            services.AddEntityFrameworkNpgsql().AddDbContext<ApiContext>(opt=>opt.UseNpgsql(_connectionString));
            //services.AddTransient<>;
        }

        // This method gets called by the runtime. Use this method to configure the HTTP request pipeline.
        public void Configure(IApplicationBuilder app, IHostingEnvironment env)
        {
            if (env.IsDevelopment())
            {
                app.UseDeveloperExceptionPage();
                app.UseCors("CorsPolicy");
            }

            app.UseMvc(async routes => routes.MapRoute(
                "default", "api/{controller}/{action}/{id?}"
            ));
        }
    }
}
