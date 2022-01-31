using Microsoft.AspNetCore.Mvc;
using WebApi.Models;
using System.Linq;

namespace WebApi.Controllers{
    [Route("api/[controller]")]
    public class SessionController : Controller{
        private readonly ApiContext _ctx;
        public SessionController(ApiContext ctx){
            _ctx = ctx;
        }
        
        // GET api/Session

        [HttpGet]
        public IActionResult GetSession()
        {
            var session = _ctx.sesja.OrderBy(c=>c.sessionid);
            return Ok(session);
        }
        
        [HttpGet("{id}",Name = "GetSession")]
        public IActionResult Get(int id){
            var session = _ctx.sesja.Find(id);
            return Ok(session);
        }

    }
}

 