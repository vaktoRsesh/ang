using System;
using System.ComponentModel.DataAnnotations;
namespace WebApi.Models
{
    public class Data{
        public int sessionid {get; set;}
        public int temperaturaot {get; set;}
        public DateTime czas {get; set;}
        public double polozenie_e {get; set;}
        public double polozenie_n {get; set;}
        public int wilgotnosc {get;set;}
        [Key]
        public int idpomiaru {get; set;}
    }
}