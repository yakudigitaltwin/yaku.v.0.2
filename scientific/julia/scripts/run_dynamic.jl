using Pkg
Pkg.activate(joinpath(@__DIR__, ".."))
using YakuDigitalTwin

r = simulate_chlorine_decay(1.5, 0.002/60, 3600.0, 60.0)
println("Yaku Julia dynamic engine")
println("C inicial = ", r.chlorine_mg_l[1], " mg/L")
println("C final   = ", r.chlorine_mg_l[end], " mg/L")
