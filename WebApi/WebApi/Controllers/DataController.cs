using Microsoft.AspNetCore.Mvc;
using WebApi.Models;
using System.Linq;

namespace WebApi.Controllers
{
    [Route("api/[controller]")]
    public class DataController : Controller{
        private readonly ApiContext _ctx;
        
        public DataController(ApiContext ctx)
        {
            _ctx = ctx;
        }

        [HttpGet]
        public IActionResult Get()
        {
            var data = _ctx.dane.OrderBy(c => c.idpomiaru);

            return Ok(data);
        }

        [HttpPost]
        public IActionResult Post([FromBody] Data data) //tego w sumie nie trzeba
        {
            if(data == null){return BadRequest();}
            _ctx.dane.Add(data);
            _ctx.SaveChanges();
            return CreatedAtRoute("GetData",new{id=data.idpomiaru},data);
        }
        
    }
}
