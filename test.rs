use elm_solve_deps::solver;
use elm_solve_deps::project_config::{ProjectConfig,AppDependencies, Pkg};
use pubgrub::error::PubGrubError;
use pubgrub::version::SemanticVersion as SemVer;
use std::path::Path;
use std::io;
use std::fs;
use std::time::{Duration, Instant};

fn main() {
    // Define an offline solver.
    let tot_start = Instant::now();
    let offline_solver = solver::Offline::new("../../registry", "0.19.1");
    let mut sol_dur = Duration::new(0, 0);
    let mut failed = 0;

    // Load the project elm.json.
    let loc = "../../registry/0.19.1/packages/";
    let providers = list_dir(Path::new(loc)).expect("error!");
    for prov in providers.iter() {
        let prov_path_string = loc.to_owned() + prov + "/";
        let pkgs = list_dir(Path::new(&prov_path_string)).expect("error!");
        for pkg in pkgs.iter() {
            println!("{}/{}:", prov, pkg);
            let d = loc.to_owned() + prov + "/" + pkg + "/";
            let p = Path::new(&d);
            let vers = list_dir(p).expect("error!");
            for ver in vers.iter() {
                let file =  d.to_owned() + ver + "/" + "elm.json";
                println!("  {}:", ver);
                let elm_json_str = std::fs::read_to_string(file)
                    .expect("Are you in an elm project? there was an issue loading the elm.json");
                let project_elm_json = serde_json::from_str(&elm_json_str)
                    .expect("Failed to decode the elm.json");
                let start = Instant::now();
                let solution = solve(project_elm_json, &offline_solver);
                let duration = start.elapsed();
                if solution.is_ok() {
                    print_solution(solution.expect("version solving failed!"));
                } else {
                    failed = failed + 1;
                }
                sol_dur = sol_dur + duration;
            }
        }
    }
    let tot_dur = tot_start.elapsed();
    println!("failed: {}", failed);
    println!("stats:");
    println!("  solving: {:?}", sol_dur);
    println!("  total: {:?}", tot_dur);
}

fn solve(project_elm_json:ProjectConfig, offline_solver:&solver::Offline) -> Result<AppDependencies, PubGrubError<Pkg, SemVer>> {
    // Solve with tests dependencies.
    let use_test = false;

    // Do not add any extra additional dependency.
    let extras = &[];

    // Solve dependencies.
    let solution = offline_solver.solve_deps(&project_elm_json, use_test, extras);
    solution
}

fn print_solution(sol:AppDependencies) {
    let mut dir = String::new();
    for (pkg, ver) in &sol.direct {
        dir += &format!("    {}: {}\n", pkg, ver);
    }
    let mut indir = String::new();
    for (pkg, ver) in &sol.indirect {
        indir += &format!("    {}: {}\n", pkg, ver);
    }
    //let s = &format!("  direct:\n{}  indirect:\n{}", &dir, &indir);
    let s = &format!("{}{}", &dir, &indir);
    println!("{}", s);
}

fn list_dir(dir: &Path) -> io::Result<Vec<String>> {
    let mut result: Vec<String> = vec![];
    if dir.is_dir() {
        for entry in fs::read_dir(dir)? {
            let entry = entry?;
            let path = entry.path();
            if path.is_dir() {
                let name = entry.file_name().into_string().expect("error converting to string");
                result.push(name);
            }
        }
    }
    Ok(result)
}
