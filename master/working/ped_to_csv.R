setwd("/homes/afohr")


load(file = "/homes/aliu/DSGE_LRS/input/r_files/ped_all_bdate.Rdata")

name <- ls()
write.csv(get(name[1]), file = "data/ped.csv")
