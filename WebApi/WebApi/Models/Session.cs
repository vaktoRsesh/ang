using System;
using System.ComponentModel.DataAnnotations;
namespace WebApi.Models
{
    public class Session{
        [Key]
        public int sessionid {get; set;}
        public DateTime dateofstart {get; set;}
        public bool sessionstatus {get; set;}
        public DateTime? dateofend {get; set;}
    }
}